import xarray as xr

import sys

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing')  # noqa: E402

import utilities.qgdynamics as qg

basedir = '/home/tcarrasco/result/data/ERA5/QGDynamic/'
filename = 'ERA5_25Jan2017_700_400.nc'

qvector = qg.qvector(basedir+filename, levi=500)
Q1, Q2, dQ, elon, elat, x, y, ug, vg, u, v, z = qvector
da = xr.DataArray(dQ, coords=[elat, elon], dims=['lat', 'lon'])
ds = xr.Dataset({'divQ': da})
ds.to_netcdf('divQ_25Jan2017.nc')
