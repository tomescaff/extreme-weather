import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import cr2met  # noqa: E402
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402

tglobal = gmst.annual_5year_smooth()
tlocal = cr2met.tmax_1d_djf_30_40S()

x = tglobal.sel(time=slice('1979', '2022'))
y = tlocal.sel(time=slice('1980', '2023'))

init_params = [37, 4, 2, 0.0]
mu0, sigma, alpha, eta = pmath.mle_gev_2d(y.values, x.values, init_params)

x_tot = np.linspace(-1.0, 5.0, 1000)
mu = mu0 + alpha*x_tot
mean = gev.mean(eta, mu, sigma)
std = gev.std(eta, mu, sigma)
mean_plus_1std = mean + std
mean_plus_2std = mean + 2*std
val_tau_10 = gev.isf(1/10, eta, mu, sigma)
val_tau_100 = gev.isf(1/100, eta, mu, sigma)

# CI
nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_CR2MET_tmax_1d_30_40S_nboot_{nboot}_gev_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)
boot_mu0 = model.mu0.values
boot_sigma = model.sigma.values
boot_alpha = model.alpha.values
boot_eta = model.eta.values

Tac = tglobal.sel(time='2017').values
Tpa = tglobal.sel(time='1880').values
Tfu = np.array([2.0])

mu_ac = mu0 + alpha*Tac
mu_pa = mu0 + alpha*Tpa
mu_fu = mu0 + alpha*Tfu

mu_ac_dist = boot_mu0 + boot_alpha*Tac
mu_pa_dist = boot_mu0 + boot_alpha*Tpa
mu_fu_dist = boot_mu0 + boot_alpha*Tfu

mu_ac_inf, mu_ac_sup = np.quantile(mu_ac_dist, [0.025, 0.975], axis=0)
mu_pa_inf, mu_pa_sup = np.quantile(mu_pa_dist, [0.025, 0.975], axis=0)
mu_fu_inf, mu_fu_sup = np.quantile(mu_fu_dist, [0.025, 0.975], axis=0)

err_mean_ac_inf = gev.mean(eta, mu_ac, sigma) - gev.mean(eta, mu_ac_inf, sigma)
err_mean_ac_sup = gev.mean(eta, mu_ac_sup, sigma) - gev.mean(eta, mu_ac, sigma)

err_mean_pa_inf = gev.mean(eta, mu_pa, sigma) - gev.mean(eta, mu_pa_inf, sigma)
err_mean_pa_sup = gev.mean(eta, mu_pa_sup, sigma) - gev.mean(eta, mu_pa, sigma)

err_mean_fu_inf = gev.mean(eta, mu_fu, sigma) - gev.mean(eta, mu_fu_inf, sigma)
err_mean_fu_sup = gev.mean(eta, mu_fu_sup, sigma) - gev.mean(eta, mu_fu, sigma)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig = plt.figure(figsize=(13, 5))
gs = fig.add_gridspec(1, 2,  width_ratios=(4, 1),
                      left=0.1, right=0.9, bottom=0.1, top=0.9,
                      wspace=0.1, hspace=0.07)

ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[0, 1], sharey=ax0)

plt.sca(ax0)
x_low = np.linspace(-1.0, x.min())
x_high = np.linspace(x.max(), 5.0)
ymin, ymax = 32, 52
plt.fill_between(x_low, ymin, ymax, color='grey', alpha=0.3)
plt.fill_between(x_high, ymin, ymax, color='grey', alpha=0.3)
plt.scatter(x, y, s=20, marker='o', edgecolor='#222831',
            facecolor='#00ADB5', alpha=0.8)

plt.plot(x_tot, mean, c='#FF2E63', lw=1.5, label='Mean')
plt.plot(x_tot, mean_plus_1std, c='#FF2E63', lw=0.5)
plt.plot(x_tot, mean_plus_2std, c='#FF2E63', lw=0.5)
plt.plot(x_tot, val_tau_100, c='#FF9A00', lw=1.5, label='100-year event')
plt.plot(x_tot, val_tau_10, c='#FF9A00',
         lw=1.5, ls='--', label='10-year event')

plt.errorbar(x=Tpa, y=gev.mean(eta, mu_pa, sigma), yerr=[
             err_mean_pa_inf, err_mean_pa_sup],
             lw=1.2, color='r', capsize=3, fmt='.', capthick=1.5)
plt.errorbar(x=Tac, y=gev.mean(eta, mu_ac, sigma), yerr=[
             err_mean_ac_inf, err_mean_ac_sup],
             lw=1.2, color='r', capsize=3, fmt='.', capthick=1.5)
plt.errorbar(x=Tfu, y=gev.mean(eta, mu_fu, sigma), yerr=[
             err_mean_fu_inf, err_mean_fu_sup],
             lw=1.2, color='r', capsize=3, fmt='.', capthick=1.5)

plt.ylim([ymin, ymax])
plt.yticks(np.arange(ymin, ymax+1, 2))
plt.xlim([-1.0, 5.0])
plt.grid(color='grey', lw=0.4, ls='--')
ax = plt.gca()
ax.tick_params(direction="in")
plt.xlabel('Global mean surface temperature anomaly (smoothed) [ºC]')
plt.ylabel('Tmax [DJF, 30-40ºS] (ºC)')
plt.legend(loc='upper center', ncol=3)

plt.sca(ax1)
y = np.linspace(ymin, ymax, 1000)
x = gev.pdf(y, eta, mu_ac, sigma)
plt.fill_betweenx(y, x, color='#00ADB5', alpha=0.8)
plt.plot(x, y, lw=0.5, c='k')
x = gev.pdf(y, eta, mu_pa, sigma)
plt.plot(x, y, lw=1, c='k', ls='--')
x = gev.pdf(y, eta, mu_fu, sigma)
plt.plot(x, y, lw=1, c='k')
plt.xlim([-0, 0.5])
plt.xlabel('PDF')
ax = plt.gca()
ax.tick_params(direction="in")
ax.yaxis.set_tick_params(length=2)
plt.axhline(gev.isf(1/100, eta, mu_ac, sigma), c='#FF9A00', lw=1.5)
plt.axhline(gev.isf(1/100, eta, mu_pa, sigma), c='#FF9A00', lw=0.5)
plt.axhline(gev.isf(1/100, eta, mu_fu, sigma), c='#FF9A00', lw=0.5)

basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_tmax_1d_GMST_gev_ext_dist.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
plt.show()
