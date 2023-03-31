import xarray as xr
import numpy as np


def tmax_1d_djf():
    basedir = '/home/tcarrasco/result/data/CR2MET/tmax/final/'
    filename = 'CR2MET_tmax_1day_DJF_1960_2023_chile_005deg.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def clmask():
    basedir = '/home/tcarrasco/result/data/CR2MET/mask/'
    filename = 'CR2MET_clmask_v2.5_mon_1960_2021_005deg.nc'
    filepath = basedir + filename
    mask = xr.open_dataset(filepath)['cl_mask']
    return mask


def tmax_1d_djf_30_40S():
    da = tmax_1d_djf()
    mask = clmask()
    da = da*mask
    da = da.where((da.lat < -30.0) & (da.lat >= -40.0), drop=True)
    ts = da.max(['lat', 'lon'])
    return ts


def area_tmax_1d_30_40S(thresold=38):
    da = tmax_1d_djf()
    mask = clmask()
    da = da*mask
    da = da.where((da.lat < -30.0) & (da.lat >= -40.0), drop=True)
    da = da.where(da >= thresold)
    da = da.count(['lat', 'lon'])
    km = 5
    da = da*km*km
    return da


def daily_tmax(year, month, day):
    bdir_ERA5T = '/mnt/cirrus/cr2met_prodution/data_folder_cr2met_ERA5T_v2_5/'
    bdir_ERA5T += 'CR2MET_out/txn/v2.5/v2.5_R1_day/'
    bdir_ERA5 = '/mnt/cirrus/cr2met_prodution/data_folder_cr2met_v2_5/'
    bdir_ERA5 += 'CR2MET_out/txn/v2.5/v2.5_R1_day/'
    filename = f'CR2MET_tmin_tmax_v2.5_R1_day_{year}_{month}_005deg.nc'
    if (float(year) == 2022 and float(month) == 11) or (float(year) >= 2023):
        basedir = bdir_ERA5T
    else:
        basedir = bdir_ERA5
    filepath = basedir + filename
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    mask = clmask()
    da = da*mask
    da = da.sel(time=f'{year}-{month}-{day}')
    return da
