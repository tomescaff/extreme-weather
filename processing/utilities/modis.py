import pandas as pd
import xarray as xr
import numpy as np


def burned_area_2017():
    basedir = '/home/tcarrasco/result/data/MCD64A1/tables/'
    dfY17D01W06 = pd.read_csv(
        basedir + 'MCD64monthly.A2017001.Win06.061.burndate.clip.csv')
    dfY17D01W07 = pd.read_csv(
        basedir + 'MCD64monthly.A2017001.Win07.061.burndate.clip.csv')
    dfY17D32W06 = pd.read_csv(
        basedir + 'MCD64monthly.A2017032.Win06.061.burndate.clip.csv')
    dfY17D32W07 = pd.read_csv(
        basedir + 'MCD64monthly.A2017032.Win07.061.burndate.clip.csv')

    DY17 = dfY17D01W06['nday'].values
    AY17 = dfY17D01W06['area'].values + \
        dfY17D01W07['area'].values + \
        dfY17D32W06['area'].values + \
        dfY17D32W07['area'].values
    data = AY17[:59]*1e-6*100*1e-3  # [1e3 Ha]
    time = pd.date_range('2017-01-01', '2017-02-28', freq='1D')
    return xr.DataArray(data, coords=[time], dims=['time'])


def burned_area_2023():
    basedir = '/home/tcarrasco/result/data/MCD64A1/tables/'
    dfY23D01W06 = pd.read_csv(
        basedir + 'MCD64monthly.A2023001.Win06.061.burndate.clip.csv')
    dfY23D01W07 = pd.read_csv(
        basedir + 'MCD64monthly.A2023001.Win07.061.burndate.clip.csv')
    dfY23D32W06 = pd.read_csv(
        basedir + 'MCD64monthly.A2023032.Win06.061.burndate.clip.csv')
    dfY23D32W07 = pd.read_csv(
        basedir + 'MCD64monthly.A2023032.Win07.061.burndate.clip.csv')

    DY23 = dfY23D01W06['nday'].values
    AY23 = dfY23D01W06['area'].values + \
        dfY23D01W07['area'].values + \
        dfY23D32W06['area'].values + \
        dfY23D32W07['area'].values
    data = AY23[:59]*1e-6*100*1e-3  # [1e3 Ha]
    time = pd.date_range('2023-01-01', '2023-02-28', freq='1D')
    return xr.DataArray(data, coords=[time], dims=['time'])


def burned_area_2017_las_maquinas():
    basedir = '/home/tcarrasco/result/data/MCD64A1/tables/'
    dfY17D01W07_LM = pd.read_csv(
        basedir +
        'MCD64monthly.A2017001.Win07.061.burndate.clip_las_maquinas_2017.csv')
    dfY17D32W07_LM = pd.read_csv(
        basedir +
        'MCD64monthly.A2017032.Win07.061.burndate.clip_las_maquinas_2017.csv')
    AY17_LM = dfY17D01W07_LM['area'].values + dfY17D32W07_LM['area'].values
    data = AY17_LM[:59]*1e-6*100*1e-3  # [1e3 Ha]
    time = pd.date_range('2017-01-01', '2017-02-28', freq='1D')
    return xr.DataArray(data, coords=[time], dims=['time'])


def burned_area_2017_complejo_concepcion():
    basedir = '/home/tcarrasco/result/data/MCD64A1/tables/'
    dfY17D01W07_CC = pd.read_csv(
        basedir +
        'MCD64monthly.A2017001.Win07.061.' +
        'burndate.clip_complejo_conce_2017.csv')
    dfY17D32W07_CC = pd.read_csv(
        basedir +
        'MCD64monthly.A2017032.Win07.061.' +
        'burndate.clip_complejo_conce_2017.csv')
    AY17_CC = dfY17D01W07_CC['area'].values + dfY17D32W07_CC['area'].values
    data = AY17_CC[:59]*1e-6*100*1e-3  # [1e3 Ha]
    time = pd.date_range('2017-01-01', '2017-02-28', freq='1D')
    return xr.DataArray(data, coords=[time], dims=['time'])


def burned_area_2023_complejo_nahuelbuta():
    basedir = '/home/tcarrasco/result/data/MCD64A1/tables/'
    dfY23D01W07_CN = pd.read_csv(
        basedir +
        'MCD64monthly.A2023001.Win07.061.' +
        'burndate.clip_complejo_nahuelbuta.csv')
    dfY23D32W07_CN = pd.read_csv(
        basedir +
        'MCD64monthly.A2023032.Win07.061.' +
        'burndate.clip_complejo_nahuelbuta.csv')
    AY23_CN = dfY23D01W07_CN['area'].values + dfY23D32W07_CN['area'].values
    data = AY23_CN[:59]*1e-6*100*1e-3  # [1e3 Ha]
    time = pd.date_range('2023-01-01', '2023-02-28', freq='1D')
    return xr.DataArray(data, coords=[time], dims=['time'])


def burned_area_2023_complejo_concepcion():
    basedir = '/home/tcarrasco/result/data/MCD64A1/tables/'
    dfY23D01W07_CC = pd.read_csv(
        basedir +
        'MCD64monthly.A2023001.Win07.061.' +
        'burndate.clip_complejo_conce_2023.csv')
    dfY23D32W07_CC = pd.read_csv(
        basedir +
        'MCD64monthly.A2023032.Win07.061.' +
        'burndate.clip_complejo_conce_2023.csv')
    AY23_CC = dfY23D01W07_CC['area'].values + dfY23D32W07_CC['area'].values
    data = AY23_CC[:59]*1e-6*100*1e-3  # [1e3 Ha]
    time = pd.date_range('2023-01-01', '2023-02-28', freq='1D')
    return xr.DataArray(data, coords=[time], dims=['time'])


def acc_burned_area(burned_area):
    time = burned_area.time
    data = burned_area.values

    acc_data = np.zeros(data.shape)
    for i in range(data.size):
        subdata = data[:(i+1)]
        acc_data[i] = np.sum(subdata)

    return xr.DataArray(acc_data, coords=[time], dims=['time'])
