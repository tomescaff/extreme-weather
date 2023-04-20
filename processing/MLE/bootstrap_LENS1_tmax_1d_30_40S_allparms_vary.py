import sys
from sklearn.utils import resample as bootstrap
import numpy as np
import xarray as xr

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402
from utilities import math as pmath  # noqa: E402

nboot = int(sys.argv[1])
assert nboot > 0, "nboot must be a positive integer"

tglobal, tlocal = metrics.lens1_data_tmax_1d()

init_params = [36.8, 1.3, 0.0, 1.1, 0.1, 0.1]
boot_mu0 = np.zeros((nboot,))
boot_sigma0 = np.zeros((nboot,))
boot_eta0 = np.zeros((nboot,))
boot_alpha = np.zeros((nboot,))
boot_beta = np.zeros((nboot,))
boot_gamma = np.zeros((nboot,))


for i in range(nboot):
    y_i, x_i = bootstrap(tlocal, tglobal)
    xopt_i = pmath.mle_gev_2d_varsig_etasig(y_i, x_i, init_params)
    boot_mu0[i] = xopt_i[0]
    boot_sigma0[i] = xopt_i[1]
    boot_eta0[i] = xopt_i[2]
    boot_alpha[i] = xopt_i[3]
    boot_beta[i] = xopt_i[4]
    boot_gamma[i] = xopt_i[5]


iter = np.arange(nboot)
model = xr.Dataset({
    'mu0':    xr.DataArray(boot_mu0,   coords=[iter], dims=['iter']),
    'sigma0':  xr.DataArray(boot_sigma0, coords=[iter], dims=['iter']),
    'eta0':    xr.DataArray(boot_eta0,   coords=[iter], dims=['iter']),
    'alpha':  xr.DataArray(boot_alpha, coords=[iter], dims=['iter']),
    'beta':    xr.DataArray(boot_beta,   coords=[iter], dims=['iter']),
    'gamma':    xr.DataArray(boot_gamma,   coords=[iter], dims=['iter'])
})

basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'MLE_LENS1_tmax_1d_30_40S_nboot_' + \
    str(nboot)+'_gev_test_allparms_var.nc'
filepath = basedir + filename
model.to_netcdf(filepath)
