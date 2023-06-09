import xarray as xr


def lens1_tmax_1d_djf_30_40S_40m():
    basedir = '/home/tcarrasco/result/data/LENS1/tmax/fldstat/'
    filename = 'CESM1_LENS_tmax_1day_DJF_1921_2100_fldmax_chile_30_40S_40m.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def lens1_tmax_1d_djf_30_40S_cr():
    basedir = '/home/tcarrasco/result/data/LENS1/tmax/fldstat/'
    filename = 'CESM1_LENS_tmax_1day_DJF_0501_2200_fldmax_chile_30_40S_cr.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def lens1_tmax_1d_djf_30_40S_40m_present():
    da = lens1_tmax_1d_djf_30_40S_40m()
    return da.sel(time=slice('2011', '2020'))


def lens1_tmax_1d_djf_30_40S_40m_future():
    da = lens1_tmax_1d_djf_30_40S_40m()
    return da.sel(time=slice('2033', '2052'))


def lens2_tmax_1d_djf_30_40S_100m():
    basedir = '/home/tcarrasco/result/data/LENS2/tmax/fldstat/'
    filename = 'CESM2_LENS_tmax_1day_DJF_1851_2100_fldmax_chile_30_40S_100m.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da
