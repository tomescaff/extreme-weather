import xarray as xr
import numpy as np
import numpy as np
import pandas as pd
import glob


def tmax_1d_djf():
    basedir = '/home/tcarrasco/result/data/CR2MET/tmax/final/'
    filename = 'CR2MET_tmax_1day_DJF_1960_2023_chile_005deg.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def tmax_3d_djf():
    basedir = '/home/tcarrasco/result/data/CR2MET/tmax/final/'
    filename = 'CR2MET_tmax_3day_DJF_1960_2023_chile_005deg.nc'
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


def tmax_3d_djf_30_40S():
    da = tmax_3d_djf()
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
    bdir_ERA5T += 'CR2MET_out/txn/v2.5/v2.5_NRT_day/'
    bdir_ERA5 = '/mnt/cirrus/cr2met_prodution/data_folder_cr2met_v2_5/'
    bdir_ERA5 += 'CR2MET_out/txn/v2.5/v2.5_R1_day/'
    fn_ERA5 = f'CR2MET_tmin_tmax_v2.5_R1_day_{year}_{month}_005deg.nc'
    fn_ERA5T = f'CR2MET_tmin_tmax_v2.5_NRT_day_{year}_{month}_005deg.nc'
    if (float(year) == 2022 and float(month) >= 11) or (float(year) >= 2023):
        filepath = bdir_ERA5T + fn_ERA5T
    else:
        filepath = bdir_ERA5 + fn_ERA5
    da = xr.open_dataset(filepath)['tmax']
    mask = clmask()
    da = da*mask
    da = da.sel(time=f'{year}-{month}-{day}')
    return da


def daily_tmin(year, month, day):
    bdir_ERA5T = '/mnt/cirrus/cr2met_prodution/data_folder_cr2met_ERA5T_v2_5/'
    bdir_ERA5T += 'CR2MET_out/txn/v2.5/v2.5_NRT_day/'
    bdir_ERA5 = '/mnt/cirrus/cr2met_prodution/data_folder_cr2met_v2_5/'
    bdir_ERA5 += 'CR2MET_out/txn/v2.5/v2.5_R1_day/'
    fn_ERA5 = f'CR2MET_tmin_tmax_v2.5_R1_day_{year}_{month}_005deg.nc'
    fn_ERA5T = f'CR2MET_tmin_tmax_v2.5_NRT_day_{year}_{month}_005deg.nc'
    if (float(year) == 2022 and float(month) >= 11) or (float(year) >= 2023):
        filepath = bdir_ERA5T + fn_ERA5T
    else:
        filepath = bdir_ERA5 + fn_ERA5
    da = xr.open_dataset(filepath)['tmin']
    mask = clmask()
    da = da*mask
    da = da.sel(time=f'{year}-{month}-{day}')
    return da


def daily_pr(year, month, day):
    bdir_ERA5T = '/mnt/cirrus/cr2met_prodution/data_folder_cr2met_ERA5T_v2_5/'
    bdir_ERA5T += 'CR2MET_out/pr/v2.5/v2.5_NRT_day/'
    bdir_ERA5 = '/mnt/cirrus/cr2met_prodution/data_folder_cr2met_v2_5/'
    bdir_ERA5 += 'CR2MET_out/pr/v2.5/v2.5_R1_day/'
    fn_ERA5 = f'CR2MET_pr_v2.5_R1_day_{year}_{month}_005deg.nc'
    fn_ERA5T = f'CR2MET_pr_v2.5_NRT_day_{year}_{month}_005deg.nc'
    if (float(year) == 2022 and float(month) >= 11) or (float(year) >= 2023):
        filepath = bdir_ERA5T + fn_ERA5T
    else:
        filepath = bdir_ERA5 + fn_ERA5
    da = xr.open_dataset(filepath)['pr']
    mask = clmask()
    da = da*mask
    da = da.sel(time=f'{year}-{month}-{day}')
    return da


def daily_clim_1991_2020(year, month, day):
    years = [str(y) for y in np.arange(1991, 2021)]
    init_year = years[0]
    da_acc = daily_tmax(init_year, month, day).squeeze()
    for y in years[1:]:
        da_acc = da_acc + daily_tmax(y, month, day).values
    da_clim = da_acc/len(years)
    return da_clim


def daily_clim_30d_nearest(year, month, day):
    year_prev = int(year)-1
    year_post = int(year)+1
    date_prev = f'{year_prev}-{month}-{day}'
    date_post = f'{year_post}-{month}-{day}'
    dr = pd.date_range(date_prev, date_post, freq='D')
    # TODO: remove leap days
    mask = dr == f'{year}-{month}-{day}'
    index = int(np.argwhere(mask))
    dates = dr[index-15: index+16]
    init_year = f'{dates[0].year}'
    init_month = f'{dates[0].month:02}'
    init_day = f'{dates[0].day:02}'
    da_acc = daily_tmax(init_year, init_month, init_day).squeeze()
    for date in dates[1:]:
        year = f'{dates[0].year}'
        month = f'{dates[0].month:02}'
        day = f'{dates[0].day:02}'
        da_acc = da_acc + daily_tmax(year, month, day).values
    da_clim = da_acc/dates.size
    return da_clim


def nday_djf(threshold=35.0):
    basedir = '/home/tcarrasco/result/data/CR2MET/nday/daily_spamax/'
    filepaths = glob.glob(basedir + '/*.nc')
    time = pd.date_range('1960', '2023', freq='1YS')
    data = np.zeros((time.size,))
    for i, filepath in enumerate(filepaths):
        da = xr.open_dataset(filepath)['tmax']
        data[i] = da.where(da >= threshold, drop=True).size
    ans = xr.DataArray(data, coords=[time], dims='time')
    return ans


def daily_spamax_djf(year='2017'):
    basedir = '/home/tcarrasco/result/data/CR2MET/nday/daily_spamax/'
    filename = 'CR2MET_tmax_v2.5_DJF_1day_'+year+'_005deg.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def boxplot_tmax_1d_djf_30_40S():
    basedir = '/home/tcarrasco/result/data/CR2MET/nday/daily_spamax/'
    time = pd.date_range('1980', '2023', freq='1YS')
    N = 90
    data = np.zeros((N, time.size))
    for i, year in enumerate(np.arange(1980, 2023+1)):
        filename = f'CR2MET_tmax_v2.5_DJF_1day_{year}_005deg.nc'
        filepath = basedir + filename
        da = xr.open_dataset(filepath)['tmax']
        data[:, i] = da.values
    return data
