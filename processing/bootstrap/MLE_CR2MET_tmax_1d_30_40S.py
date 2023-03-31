import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from sklearn.utils import resample as bootstrap

sys.path.append('../../processing')

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import cr2met  # noqa: E402
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402


tglobal = gmst.annual_5year_smooth()
tlocal = cr2met.tmax_1d_djf_30_40S()

x = tglobal.sel(time=slice('1979', '2022'))
y = tlocal.sel(time=slice('1980', '2023'))

# bootstrap
nboot = 10000
bspreds_mu0 = np.zeros((nboot,))
bspreds_sigma = np.zeros((nboot,))
bspreds_alpha = np.zeros((nboot,))
bspreds_eta = np.zeros((nboot,))

for i in range(nboot):
    y_i, x_i = bootstrap(y.values, x.values)
    init_params = [37, 4, 2, 0.1, 0.0]
    xopt_i = pmath.mle_gev_2d(y_i, x_i, init_params)
    bspreds_mu0[i] = xopt_i[0]
    bspreds_sigma[i] = xopt_i[1]
    bspreds_alpha[i] = xopt_i[2]
    bspreds_eta[i] = xopt_i[3]

iter = np.arange(nboot)
ds = xr.Dataset({
    'mu0':    xr.DataArray(bspreds_mu0,    coords=[iter], dims=['iter']),
    'sigma': xr.DataArray(bspreds_sigma, coords=[iter], dims=['iter']),
    'alpha':  xr.DataArray(bspreds_alpha,  coords=[iter], dims=['iter']),
    'eta':  xr.DataArray(bspreds_eta,  coords=[iter], dims=['iter'])
})
basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_nboot_'+str(nboot)+'_gev_evaluation.nc'
filepath = basedir + filename
ds.to_netcdf(filepath)
