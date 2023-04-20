import pandas as pd
import xarray as xr
from os.path import join
import statsmodels.api as sm


def annual_global_HadCRUT():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'HadCRUT.5.0.1.0.analysis.summary_series.global.annual.csv'
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, parse_dates={'time': ['Time']})
    df.rename(columns={'Time': 'time',
                       'Anomaly (deg C)': 'anom',
                       'Lower confidence limit (2.5%)': 'lower',
                       'Upper confidence limit (97.5%)': 'upper'},
              inplace=True)
    df = df.set_index('time')
    ds = df.to_xarray().astype(float)
    ds = ds - ds.sel(time=slice('1850', '1900')).mean('time')
    ds = ds.sel(time=slice('1850', '2022'))
    return ds


def annual_global_HadCRUT_5year_smooth():
    gmst = annual_global_HadCRUT()['anom']
    n = gmst.size
    smooth_gmst = sm.nonparametric.lowess(
        gmst.values, gmst.time.dt.year, frac=10./n)
    da = xr.DataArray(smooth_gmst[:, 1], coords=[gmst.time], dims=['time'])
    return da


def annual_5year_smooth():
    return annual_global_HadCRUT_5year_smooth()


def annual_global_GISTEMP_lowess_from_csv():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'GISTEMP_year_smooth_2022.csv'
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, skiprows=1, parse_dates={'time': ['Year']})
    df = df.set_index('time')
    return df['Lowess(5)'].to_xarray().astype(float)


def annual_global_GISTEMP():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'GISTEMP_year_smooth_2022.csv'
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, skiprows=1, parse_dates={'time': ['Year']})
    df = df.set_index('time')
    return df['No_Smoothing'].to_xarray().astype(float)


def annual_global_GISTEMP_5year_smooth():
    gmst = annual_global_GISTEMP()
    n = gmst.size
    smooth_gmst = sm.nonparametric.lowess(
        gmst.values, gmst.time.dt.year, frac=10./n)
    da = xr.DataArray(smooth_gmst[:, 1], coords=[gmst.time], dims=['time'])
    return da


def annual_lens1_cr_full_values():
    basedir = '/home/tcarrasco/result/data/LENS1/tas/final/'
    filename = 'CESM1_LENS_tas_annual_0500_2199_global_mean_cr.nc'
    filepath = join(basedir, filename)
    da = xr.open_dataset(filepath)['TREFHT'] - 273.15
    return da


def annual_lens1_cr():
    da = annual_lens1_cr_full_values()
    da_anom = da-da.mean('time')
    return da_anom


def annual_lens1_ensmean():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'tas_CESM1-CAM5_LENS_ensmean_spamean_yearmean.nc'
    filepath = join(basedir, filename)
    da_lens1 = xr.open_dataset(filepath)['tas'] - 273.15

    da_anom = da_lens1 - annual_lens1_cr_full_values().mean('time')
    return da_anom


def annual_lens2_ensmean():
    basedir = '/home/tcarrasco/result/data/GMST'
    filename = 'tas_CESM2_LENS_ensmean_spamean_yearmean.nc'
    filepath = join(basedir, filename)
    da = xr.open_dataset(filepath)['tas'] - 273.15
    da_anom = da - da.sel(time=slice('1850', '1900')).mean('time')
    return da_anom
