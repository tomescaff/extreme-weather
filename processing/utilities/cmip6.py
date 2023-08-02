import xarray as xr


def access_tmax_1d_djf_30_40S_40m():
    basedir = '/home/tcarrasco/result/data/ACCESS/tmax/fldstat/'
    filename = 'ACCESS_tmax_1day_DJF_1851_2014_fldmax_chile_30_40S_40m.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def access_tas_annual_fldmean_ensmean():
    basedir = '/home/tcarrasco/result/data/ACCESS/tas/final/HIST/'
    filename = 'tas_ACCESS_ensmean_spamean_yearmean_HIST.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tas'].squeeze() - 273.15
    da_anom = da - da.sel(time=slice('1850', '1900')).mean('time')
    return da_anom


def ecearth3_tmax_1d_djf_30_40S_22m():
    basedir = '/home/tcarrasco/result/data/ECEarth3/tmax/fldstat/'
    filename = 'ECEarth3_tmax_1day_DJF_1851_2014_fldmax_chile_30_40S_22m.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def ecearth3_tas_annual_fldmean_ensmean():
    basedir = '/home/tcarrasco/result/data/ECEarth3/tas/final/HIST/'
    filename = 'tas_ECEarth3_ensmean_spamean_yearmean_HIST.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tas'].squeeze() - 273.15
    da_anom = da - da.sel(time=slice('1850', '1900')).mean('time')
    return da_anom
