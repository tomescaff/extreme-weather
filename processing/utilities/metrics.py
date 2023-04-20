import xarray as xr
import numpy as np
import pandas as pd
from scipy.stats import genextreme as gev
from scipy.stats import norm
from sklearn.utils import resample as bootstrap
from . import math as pmath
from . import lens
from . import cr2met
from . import gmst


def obs_data_tmax_1d():
    tglobal = gmst.annual_5year_smooth()
    tlocal = cr2met.tmax_1d_djf_30_40S()
    x = tglobal.sel(time=slice('1979', '2022')).values
    y = tlocal.sel(time=slice('1980', '2023')).values
    return x, y


def obs_data_tmax_1d_remove_year(tlocal_year_to_remove=[]):
    tglobal = gmst.annual_5year_smooth()
    tlocal = cr2met.tmax_1d_djf_30_40S()
    for yr in tlocal_year_to_remove:
        prev_yr = yr-1
        tglobal = tglobal.where(tglobal.time.dt.year != prev_yr, drop=True)
        tlocal = tlocal.where(tlocal.time.dt.year != yr, drop=True)
    x = tglobal.sel(time=slice('1979', '2022')).values
    y = tlocal.sel(time=slice('1980', '2023')).values
    return x, y


def lens1_data_tmax_1d():
    tglobal = gmst.annual_lens1_ensmean()
    tlocal = lens.lens1_tmax_1d_djf_30_40S_40m()
    tglobal = tglobal.sel(time=slice('1920', '2099'))
    tlocal = tlocal.sel(time=slice('1921', '2100'))  # 40 ensemble members
    x = np.tile(tglobal.values, tlocal.shape[1])
    y = np.ravel(tlocal.values, order='F')
    return x, y


def lens1_data_tmax_1d_1980_2023():
    tglobal = gmst.annual_lens1_ensmean()
    tlocal = lens.lens1_tmax_1d_djf_30_40S_40m()
    tglobal = tglobal.sel(time=slice('1979', '2022'))
    tlocal = tlocal.sel(time=slice('1980', '2023'))  # 40 ensemble members
    x = np.tile(tglobal.values, tlocal.shape[1])
    y = np.ravel(tlocal.values, order='F')
    return x, y


def lens1_data_tmax_1d_1980_2023_ensemble(ens=0, tlocal_year_to_remove=[]):
    tglobal = gmst.annual_lens1_ensmean()
    tlocal = lens.lens1_tmax_1d_djf_30_40S_40m()
    tglobal = tglobal.sel(time=slice('1979', '2022'))
    tlocal = tlocal.sel(time=slice('1980', '2023')).sel(
        ensemble=ens)  # 1 ensemble member
    for yr in tlocal_year_to_remove:
        prev_yr = yr-1
        tglobal = tglobal.where(tglobal.time.dt.year != prev_yr, drop=True)
        tlocal = tlocal.where(tlocal.time.dt.year != yr, drop=True)

    x = tglobal.values
    y = tlocal.values
    return x, y


def lens1_data_tmax_1d_1980_2023_bias_corrected():
    tglobal = gmst.annual_lens1_ensmean()
    tlocal = lens.lens1_tmax_1d_djf_30_40S_40m()
    tobs = cr2met.tmax_1d_djf_30_40S()

    tglobal = tglobal.sel(time=slice('1920', '2099'))
    tlocal = tlocal.sel(time=slice('1921', '2100'))  # 40 ensemble members
    bias = tlocal.sel(time=slice('1980', '2023')).mean('time') - \
        tobs.sel(time=slice('1980', '2023')).mean('time')
    tlocal = tlocal - bias

    tglobal = tglobal.sel(time=slice('1979', '2022'))
    tlocal = tlocal.sel(time=slice('1980', '2023'))
    x = np.tile(tglobal.values, tlocal.shape[1])
    y = np.ravel(tlocal.values, order='F')
    return x, y


def bootstrap_tau_gev(model, tglobal, tlocal):
    boot_mu0 = model.mu0.values
    boot_sigma = model.sigma.values
    boot_alpha = model.alpha.values
    boot_eta = model.eta.values
    boot_mu_ac = boot_mu0 + boot_alpha*tglobal
    boot_tau_ac = model.mu0.copy()
    boot_tau_ac[:] = 1/gev.sf(tlocal, boot_eta, boot_mu_ac, boot_sigma)
    model['tau'] = boot_tau_ac
    return model


def bootstrap_tau_norm(model, tglobal, tlocal):
    boot_mu0 = model.mu0.values
    boot_sigma = model.sigma.values
    boot_alpha = model.alpha.values
    boot_mu_ac = boot_mu0 + boot_alpha*tglobal
    boot_tau_ac = model.mu0.copy()
    boot_tau_ac[:] = 1/norm.sf(tlocal, boot_mu_ac, boot_sigma)
    model['tau'] = boot_tau_ac
    return model


def bootstrap_gev(tglobal, tlocal, nboot,
                  init_params=[36.8, 1.3, 1.1, 0.1]):
    boot_mu0 = np.zeros((nboot,))
    boot_sigma = np.zeros((nboot,))
    boot_alpha = np.zeros((nboot,))
    boot_eta = np.zeros((nboot,))

    for i in range(nboot):
        y_i, x_i = bootstrap(tlocal, tglobal)
        xopt_i = pmath.mle_gev_2d(y_i, x_i, init_params)
        boot_mu0[i] = xopt_i[0]
        boot_sigma[i] = xopt_i[1]
        boot_alpha[i] = xopt_i[2]
        boot_eta[i] = xopt_i[3]

    iter = np.arange(nboot)
    model = xr.Dataset({
        'mu0':    xr.DataArray(boot_mu0,   coords=[iter], dims=['iter']),
        'sigma':  xr.DataArray(boot_sigma, coords=[iter], dims=['iter']),
        'alpha':  xr.DataArray(boot_alpha, coords=[iter], dims=['iter']),
        'eta':    xr.DataArray(boot_eta,   coords=[iter], dims=['iter'])
    })
    return model


def bootstrap_norm(tglobal, tlocal, nboot,
                   init_params=[36.8, 1.3, 1.1]):
    boot_mu0 = np.zeros((nboot,))
    boot_sigma = np.zeros((nboot,))
    boot_alpha = np.zeros((nboot,))

    for i in range(nboot):
        y_i, x_i = bootstrap(tlocal, tglobal)
        xopt_i = pmath.mle_norm_2d(y_i, x_i, init_params)
        boot_mu0[i] = xopt_i[0]
        boot_sigma[i] = xopt_i[1]
        boot_alpha[i] = xopt_i[2]

    iter = np.arange(nboot)
    model = xr.Dataset({
        'mu0':    xr.DataArray(boot_mu0,   coords=[iter], dims=['iter']),
        'sigma':  xr.DataArray(boot_sigma, coords=[iter], dims=['iter']),
        'alpha':  xr.DataArray(boot_alpha, coords=[iter], dims=['iter']),
    })
    return model


def tau_best_estimate_gev(tglobal, tlocal, climate_gmst, ee_value,
                          init_params=[37, 4, 2, 0.0]):
    mu0, sigma, alpha, eta = pmath.mle_gev_2d(tlocal, tglobal, init_params)
    mu = mu0 + alpha*climate_gmst
    return 1/gev.sf(ee_value, eta, mu, sigma)


def tau_best_estimate_norm(tglobal, tlocal, climate_gmst, ee_value,
                           init_params=[37, 4, 2]):
    mu0, sigma, alpha = pmath.mle_norm_2d(tlocal, tglobal, init_params)
    mu = mu0 + alpha*climate_gmst
    return 1/norm.sf(ee_value, mu, sigma)


def gev_best_estimate(tglobal, tlocal,
                      init_params=[36.8, 1.3, 1.1, 0.1]):

    mu0, sigma, alpha, eta = pmath.mle_gev_2d(tlocal, tglobal, init_params)

    indx = ['Best estimate']
    cols = ['mu0', 'sigma', 'alpha', 'eta']
    df = pd.DataFrame(index=indx, columns=cols)

    df.loc['Best estimate', 'mu0'] = mu0
    df.loc['Best estimate', 'sigma'] = sigma
    df.loc['Best estimate', 'alpha'] = alpha
    df.loc['Best estimate', 'eta'] = eta

    return df


def norm_best_estimate(tglobal, tlocal,
                       init_params=[36.8, 1.3, 1.1]):

    mu0, sigma, alpha = pmath.mle_norm_2d(tlocal, tglobal, init_params)

    indx = ['Best estimate']
    cols = ['mu0', 'sigma', 'alpha']
    df = pd.DataFrame(index=indx, columns=cols)

    df.loc['Best estimate', 'mu0'] = mu0
    df.loc['Best estimate', 'sigma'] = sigma
    df.loc['Best estimate', 'alpha'] = alpha

    return df


def MLE_all_estimate(df, model, Tg_ac, Tg_pa=0.0, Tg_fu=2.0):

    mu0 = df.loc['Best estimate', 'mu0']
    sigma = df.loc['Best estimate', 'sigma']
    alpha = df.loc['Best estimate', 'alpha']
    eta = df.loc['Best estimate', 'eta']

    mu_ac = mu0 + alpha*Tg_ac
    mu_pa = mu0 + alpha*Tg_pa
    mu_fu = mu0 + alpha*Tg_fu

    tau = 100
    ev_ac = gev.isf(1/tau, eta, mu_ac, sigma)
    ev_pa = gev.isf(1/tau, eta, mu_pa, sigma)
    ev_fu = gev.isf(1/tau, eta, mu_fu, sigma)

    deltaI_fu_ac = ev_fu - ev_ac
    deltaI_ac_pa = ev_ac - ev_pa

    tau_ac = 1/gev.sf(ev_ac, eta, mu_ac, sigma)
    tau_pa = 1/gev.sf(ev_ac, eta, mu_pa, sigma)
    tau_fu = 1/gev.sf(ev_ac, eta, mu_fu, sigma)

    PR_fu_ac = tau_ac/tau_fu
    PR_ac_pa = tau_pa/tau_ac

    df.loc['Best estimate', 'tau_ac'] = tau_ac
    df.loc['Best estimate', 'tau_pa'] = tau_pa
    df.loc['Best estimate', 'tau_fu'] = tau_fu

    df.loc['Best estimate', 'ev_ac'] = ev_ac
    df.loc['Best estimate', 'ev_pa'] = ev_pa
    df.loc['Best estimate', 'ev_fu'] = ev_fu

    df.loc['Best estimate', 'Delta fu-ac'] = deltaI_fu_ac
    df.loc['Best estimate', 'Delta ac-pa'] = deltaI_ac_pa

    df.loc['Best estimate', 'PR fu-ac'] = PR_fu_ac
    df.loc['Best estimate', 'PR ac-pa'] = PR_ac_pa

    nboot = model.iter.size
    boot_mu0 = model.mu0.values
    boot_sigma = model.sigma.values
    boot_alpha = model.alpha.values
    boot_eta = model.eta.values

    boot_tau_ac = np.zeros((nboot,))
    boot_tau_pa = np.zeros((nboot,))
    boot_tau_fu = np.zeros((nboot,))

    boot_ev_ac = np.zeros((nboot,))
    boot_ev_pa = np.zeros((nboot,))
    boot_ev_fu = np.zeros((nboot,))

    boot_deltaI_fu_ac = np.zeros((nboot,))
    boot_deltaI_ac_pa = np.zeros((nboot,))

    boot_PR_fu_ac = np.zeros((nboot,))
    boot_PR_ac_pa = np.zeros((nboot,))

    for i in range(nboot):
        mu0 = boot_mu0[i]
        sigma = boot_sigma[i]
        alpha = boot_alpha[i]
        eta = boot_eta[i]

        mu_ac = mu0 + alpha*Tg_ac
        mu_pa = mu0 + alpha*Tg_pa
        mu_fu = mu0 + alpha*Tg_fu

        tau = 100
        boot_ev_ac[i] = gev.isf(1/tau, eta, mu_ac, sigma)
        boot_ev_pa[i] = gev.isf(1/tau, eta, mu_pa, sigma)
        boot_ev_fu[i] = gev.isf(1/tau, eta, mu_fu, sigma)

        boot_deltaI_fu_ac[i] = boot_ev_fu[i] - boot_ev_ac[i]
        boot_deltaI_ac_pa[i] = boot_ev_ac[i] - boot_ev_pa[i]

        boot_tau_ac[i] = 1/gev.sf(ev_ac, eta, mu_ac, sigma)
        boot_tau_pa[i] = 1/gev.sf(ev_ac, eta, mu_pa, sigma)
        boot_tau_fu[i] = 1/gev.sf(ev_ac, eta, mu_fu, sigma)

        boot_PR_fu_ac[i] = boot_tau_ac[i]/boot_tau_fu[i]
        boot_PR_ac_pa[i] = boot_tau_pa[i]/boot_tau_ac[i]

    # ###

    df.loc['Lower estimate', 'mu0'] = np.quantile(boot_mu0, 0.025)
    df.loc['Lower estimate', 'sigma'] = np.quantile(boot_sigma, 0.025)
    df.loc['Lower estimate', 'alpha'] = np.quantile(boot_alpha, 0.025)
    df.loc['Lower estimate', 'eta'] = np.quantile(boot_eta, 0.025)

    df.loc['Lower estimate', 'tau_ac'] = np.quantile(boot_tau_ac, 0.025)
    df.loc['Lower estimate', 'tau_pa'] = np.quantile(boot_tau_pa, 0.025)
    df.loc['Lower estimate', 'tau_fu'] = np.quantile(boot_tau_fu, 0.025)

    df.loc['Lower estimate', 'ev_ac'] = np.quantile(boot_ev_ac, 0.025)
    df.loc['Lower estimate', 'ev_pa'] = np.quantile(boot_ev_pa, 0.025)
    df.loc['Lower estimate', 'ev_fu'] = np.quantile(boot_ev_fu, 0.025)

    df.loc['Lower estimate',
           'Delta fu-ac'] = np.quantile(boot_deltaI_fu_ac, 0.025)
    df.loc['Lower estimate',
           'Delta ac-pa'] = np.quantile(boot_deltaI_ac_pa, 0.025)

    df.loc['Lower estimate', 'PR fu-ac'] = np.quantile(boot_PR_fu_ac, 0.025)
    df.loc['Lower estimate', 'PR ac-pa'] = np.quantile(boot_PR_ac_pa, 0.025)

    # ###

    df.loc['Upper estimate', 'mu0'] = np.quantile(boot_mu0, 0.975)
    df.loc['Upper estimate', 'sigma'] = np.quantile(boot_sigma, 0.975)
    df.loc['Upper estimate', 'alpha'] = np.quantile(boot_alpha, 0.975)
    df.loc['Upper estimate', 'eta'] = np.quantile(boot_eta, 0.975)

    df.loc['Upper estimate', 'tau_ac'] = np.quantile(boot_tau_ac, 0.975)
    df.loc['Upper estimate', 'tau_pa'] = np.quantile(boot_tau_pa, 0.975)
    df.loc['Upper estimate', 'tau_fu'] = np.quantile(boot_tau_fu, 0.975)

    df.loc['Upper estimate', 'ev_ac'] = np.quantile(boot_ev_ac, 0.975)
    df.loc['Upper estimate', 'ev_pa'] = np.quantile(boot_ev_pa, 0.975)
    df.loc['Upper estimate', 'ev_fu'] = np.quantile(boot_ev_fu, 0.975)

    df.loc['Upper estimate',
           'Delta fu-ac'] = np.quantile(boot_deltaI_fu_ac, 0.975)
    df.loc['Upper estimate',
           'Delta ac-pa'] = np.quantile(boot_deltaI_ac_pa, 0.975)

    df.loc['Upper estimate', 'PR fu-ac'] = np.quantile(boot_PR_fu_ac, 0.975)
    df.loc['Upper estimate', 'PR ac-pa'] = np.quantile(boot_PR_ac_pa, 0.975)

    return df


def MLE_all_estimate_gev(df, model):

    boot_mu0 = model.mu0.values
    boot_sigma = model.sigma.values
    boot_alpha = model.alpha.values
    boot_eta = model.eta.values

    # ###

    df.loc['Lower estimate', 'mu0'] = np.quantile(boot_mu0, 0.025)
    df.loc['Lower estimate', 'sigma'] = np.quantile(boot_sigma, 0.025)
    df.loc['Lower estimate', 'alpha'] = np.quantile(boot_alpha, 0.025)
    df.loc['Lower estimate', 'eta'] = np.quantile(boot_eta, 0.025)

    # ###

    df.loc['Upper estimate', 'mu0'] = np.quantile(boot_mu0, 0.975)
    df.loc['Upper estimate', 'sigma'] = np.quantile(boot_sigma, 0.975)
    df.loc['Upper estimate', 'alpha'] = np.quantile(boot_alpha, 0.975)
    df.loc['Upper estimate', 'eta'] = np.quantile(boot_eta, 0.975)

    return df
