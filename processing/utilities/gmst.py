import pandas as pd
import xarray as xr
from os.path import join


def annual_5year_smooth():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'GMST_year_smooth_2022.csv'
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, skiprows=1, parse_dates={'time': ['Year']})
    df = df.set_index('time')
    return df['Lowess(5)'].to_xarray().astype(float)


def annual_lens1_ensmean():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'tas_CESM1-CAM5_LENS_ensmean_spamean_yearmean.nc'
    filepath = join(basedir, filename)
    da = xr.open_dataset(filepath)['tas'] - 273.15
    da_anom = da - da.sel(time=slice('1951', '1980')).mean('time')
    return da_anom


def annual_lens2_ensmean():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'tas_CESM2_LENS_ensmean_spamean_yearmean.nc'
    filepath = join(basedir, filename)
    da = xr.open_dataset(filepath)['tas'] - 273.15
    da_anom = da - da.sel(time=slice('1951', '1980')).mean('time')
    return da_anom
