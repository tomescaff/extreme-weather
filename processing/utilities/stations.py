from os.path import join
import xarray as xr
import numpy as np
import pandas as pd


def qn_tmax_daily_1911_2023():
    basedir = "/home/tcarrasco/result/data/QN/"
    filename = "T_maxima_diaria_QN_1911_2023.csv"
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, decimal=",", sep=';')
    df = df.loc[:, "1911":"2023"].astype(float)
    data = np.ravel(df.values, order='F')
    time = pd.date_range('1911-01-01', '2023-12-31', freq='1D')
    noleap = time[(time.day != 29) | (time.month != 2)]
    da = xr.DataArray(data, coords=[noleap], dims=['time'])
    return da


def cu_tmax_daily_1958_2023():
    basedir = "/home/tcarrasco/result/data/CU/"
    filename = "tmax_diaria_general_freire_CR2_explorador.csv"
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, delimiter=",", decimal=".",
                     parse_dates={'time': ['agno', ' mes', ' dia']})
    df = df.rename({' valor': 'tmax'}, axis='columns')
    df = df.set_index('time')
    da = df['tmax'].to_xarray()
    da = da.sel(time=slice('1958-04-01', None))
    month = da.time.dt.month
    day = da.time.dt.day
    da = xr.where((month == 2) & (day == 29), np.nan, da)
    da = da.dropna(dim="time", how="any")
    return da


def ch_tmax_daily_1960_2023():
    basedir = "/home/tcarrasco/result/data/CH/"
    filename = "tmax_diaria_bernardo_ohiggins_CR2_explorador.csv"
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, delimiter=",", decimal=".",
                     parse_dates={'time': ['agno', ' mes', ' dia']})
    df = df.rename({' valor': 'tmax'}, axis='columns')
    df = df.set_index('time')
    da = df['tmax'].to_xarray()
    da = da.sel(time=slice('1960-01-01', None))
    month = da.time.dt.month
    day = da.time.dt.day
    da = xr.where((month == 2) & (day == 29), np.nan, da)
    da = da.dropna(dim="time", how="any")
    return da


def te_tmax_daily_1960_2023():
    basedir = "/home/tcarrasco/result/data/TE/"
    filename = "tmax_diaria_temuco_CR2_explorador.csv"
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, delimiter=",", decimal=".",
                     parse_dates={'time': ['agno', ' mes', ' dia']})
    df = df.rename({' valor': 'tmax'}, axis='columns')
    df = df.set_index('time')
    da = df['tmax'].to_xarray()
    da = da.sel(time=slice('1960-01-01', None))
    month = da.time.dt.month
    day = da.time.dt.day
    da = xr.where((month == 2) & (day == 29), np.nan, da)
    da = da.dropna(dim="time", how="any")
    return da


def la_tmax_daily_1960_2023():
    basedir = "/home/tcarrasco/result/data/LA/"
    filename = "tmax_diaria_los_angeles_CR2_explorador.csv"
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, delimiter=",", decimal=".",
                     parse_dates={'time': ['agno', ' mes', ' dia']})
    df = df.rename({' valor': 'tmax'}, axis='columns')
    df = df.set_index('time')
    da = df['tmax'].to_xarray()
    da = da.sel(time=slice('1960-01-01', None))
    month = da.time.dt.month
    day = da.time.dt.day
    da = xr.where((month == 2) & (day == 29), np.nan, da)
    da = da.dropna(dim="time", how="any")
    return da


def tch_wind_2023():
    basedir = "/home/tcarrasco/result/data/TCH/"
    filename = "termas_chillan_viento_maximo_2023.csv"
    filepath = join(basedir, filename)
    df = pd.read_csv(filepath, delimiter=",", decimal=".",
                     parse_dates={'time': ['Anho', 'Mes', 'Dia']})
    df = df.rename({'Fuerza Viento Max (Kt)': 'ff'}, axis='columns')
    df = df.set_index('time')
    da = df['ff'].to_xarray()
    da = da.sel(time=slice('1960-01-01', None))
    month = da.time.dt.month
    day = da.time.dt.day
    da = xr.where((month == 2) & (day == 29), np.nan, da)
    da = da.dropna(dim="time", how="any")
    return da


def select_station(stn):
    available = {}
    available['qn'] = (qn_tmax_daily_1911_2023, '1911', '2023')
    available['cu'] = (cu_tmax_daily_1958_2023, '1958', '2023')
    available['ch'] = (cu_tmax_daily_1958_2023, '1960', '2023')
    return available[stn]


def tmax_1d_DJF(stn):
    fun, ini, end = select_station(stn)
    da = fun()
    da = da.sel(time=slice(f'{ini}-12-01', f'{end}-02-28'))
    da = da.where(da.time.dt.month.isin([12, 1, 2]), drop=True)
    # da = da.coarsen(time=90).max()
    da = da.resample(time='AS-Dec').max(skipna=True)
    return da


def tmax_3d_DJF(stn):
    fun, ini, end = select_station(stn)
    da = fun()
    da = da.rolling(time=3, center=True).mean()
    da = da.sel(time=slice(f'{ini}-12-01', f'{end}-02-28'))
    da = da.where(da.time.dt.month.isin([12, 1, 2]), drop=True)
    month = da.time.dt.month
    day = da.time.dt.day
    da = xr.where((month == 2) & (day == 28), np.nan, da)
    da = xr.where((month == 12) & (day == 1), np.nan, da)
    da = da.dropna(dim="time", how="any")
    # da = da.coarsen(time=88).max()
    da = da.resample(time='AS-Dec').max(skipna=True)
    return da


def fill_na(data_array, start_date='2017-01-01', end_date='2017-02-28'):
    dr = pd.date_range(start_date, end_date, freq='1D')
    da_ans = xr.DataArray(np.zeros((dr.size,))*np.nan,
                          coords=[dr],
                          dims=['time'])
    for i, date in enumerate(dr):
        try:
            da_ans[i] = data_array.sel(time=date)
        except Exception as e:
            continue
    return da_ans
