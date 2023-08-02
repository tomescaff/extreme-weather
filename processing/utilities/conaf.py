import pandas as pd
import numpy as np
import xarray as xr
import openpyxl


def burned_area():
    basedir = "/home/tcarrasco/result/data/CONAF/"
    filename = "resumen_nacional_ocurrencia_dano_1964_2022.xlsx"
    filepath = basedir + filename
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook['Historico']
    years = np.arange(1964, 2022+1)
    N = years.size
    data = np.zeros((N+1,))
    for i in range(N):
        data[i] = float(sheet.cell(row=11+i, column=6).value)
    data[N] = 432000
    dr = pd.date_range('1964-01-01', '2023-01-01', freq='1YS')
    da = xr.DataArray(data, coords=[dr], dims=['time'])
    return da
