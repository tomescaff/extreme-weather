import pandas as pd
import numpy as np
import xarray as xr
import sys
from datetime import datetime

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

import utilities.cr2met as cr2met  # noqa: E402


def dateparse(x): return datetime.strptime(x, '%d/%m/%Y')


df = pd.read_csv('TAR.txt', header=None)
dates = pd.to_datetime(df[0], format="%d/%m/%Y")

date = dates[0]
pr_day = cr2met.daily_pr(f'{date.year:04d}',
                         f'{date.month:02d}',
                         f'{date.day:02d}')

lat = pr_day.lat
lon = pr_day.lon
time = dates

ntime, nlat, nlon = time.size, lat.size, lon.size

data_pr = np.zeros((ntime, nlat, nlon))*np.nan
data_tmin = np.zeros((ntime, nlat, nlon))*np.nan
data_tmax = np.zeros((ntime, nlat, nlon))*np.nan

for i, date in enumerate(dates):
    print(date)
    pr_day = cr2met.daily_pr(f'{date.year:04d}',
                             f'{date.month:02d}',
                             f'{date.day:02d}')
    tmin_day = cr2met.daily_tmin(f'{date.year:04d}',
                                 f'{date.month:02d}',
                                 f'{date.day:02d}')
    tmax_day = cr2met.daily_tmax(f'{date.year:04d}',
                                 f'{date.month:02d}',
                                 f'{date.day:02d}')

    data_pr[i, :, :] = pr_day.values
    data_tmin[i, :, :] = tmin_day.values
    data_tmax[i, :, :] = tmax_day.values

da_pr = xr.DataArray(data_pr, [time, lat, lon], dims=['time', 'lat', 'lon'])
da_tmin = xr.DataArray(data_tmin, [time, lat, lon], dims=[
                       'time', 'lat', 'lon'])
da_tmax = xr.DataArray(data_tmax, [time, lat, lon], dims=[
                       'time', 'lat', 'lon'])
dsout = xr.Dataset({'pr': da_pr, 'tmin': da_tmin, 'tmax': da_tmax})
dsout.to_netcdf('TAR_RDG.nc')
