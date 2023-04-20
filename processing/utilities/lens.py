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
