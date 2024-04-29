"""CMIP6 data access functions.

This module contains functions to access CMIP6 data stored in CR2's data 
servers. It contains the following functions:

    * access_tmax_1d_djf_30_40S_40m: Access xTx 40-member ensemble from 
        the ACCESS-ESM1-5 model for Chilean region between 30-40S.
        
    * access_tas_annual_fldmean_ensmean: Access GSAT 40-member ensemble 
        mean from the ACCESS-ESM1-5 model.
    
    * ecearth3_tmax_1d_djf_30_40S_22m: Access xTx 22-member ensemble 
        from the EC-Earth3 model for Chilean region between 30-40S.
    
    * ecearth3_tas_annual_fldmean_ensmean: Access GSAT 22-member
        ensemble mean from the EC-Earth3 model.  
"""


import xarray as xr


def access_tmax_1d_djf_30_40s_40m():
    """Access xTx 40-member ensemble from the ACCESS-ESM1-5 model for 
    Chilean region between 30-40S.

    Returns
    -------
    xr.DataArray
        xTx data for the Chilean region between 30-40S from 1850/51 to
        2013/14.
    """
    basedir = '/home/tcarrasco/result/data/ACCESS/tmax/fldstat/'
    filename = 'ACCESS_tmax_1day_DJF_1851_2014_fldmax_chile_30_40S_40m.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def access_tas_annual_fldmean_ensmean():
    """Access GSAT 40-member ensemble mean from the ACCESS-ESM1-5 model.

    Returns
    -------
    xr.DataArray
        GSAT anomaly (ºC) [wrt 1850-1900] for the globe from 1850 to 
        2014.
    """

    basedir = '/home/tcarrasco/result/data/ACCESS/tas/final/HIST/'
    filename = 'tas_ACCESS_ensmean_spamean_yearmean_HIST.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tas'].squeeze() - 273.15
    da_anom = da - da.sel(time=slice('1850', '1900')).mean('time')
    return da_anom


def ecearth3_tmax_1d_djf_30_40s_22m():
    """Access xTx 40-member ensemble from the EC-Earth3 model for 
    Chilean region between 30-40S.

    Returns
    -------
    xr.DataArray
        xTx data for the Chilean region between 30-40S from 1850/51 to
        2013/14.
    """
    basedir = '/home/tcarrasco/result/data/ECEarth3/tmax/fldstat/'
    filename = 'ECEarth3_tmax_1day_DJF_1851_2014_fldmax_chile_30_40S_22m.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tmax']
    return da


def ecearth3_tas_annual_fldmean_ensmean():
    """Access GSAT 40-member ensemble mean from the EC-Earth3 model.

    Returns
    -------
    xr.DataArray
        GSAT anomaly (ºC) [wrt 1850-1900] for the globe from 1850 to 
        2014.
    """
    basedir = '/home/tcarrasco/result/data/ECEarth3/tas/final/HIST/'
    filename = 'tas_ECEarth3_ensmean_spamean_yearmean_HIST.nc'
    filepath = basedir + filename
    da = xr.open_dataset(filepath)['tas'].squeeze() - 273.15
    da_anom = da - da.sel(time=slice('1850', '1900')).mean('time')
    return da_anom
