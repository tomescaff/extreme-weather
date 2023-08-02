import pandas as pd
import xarray as xr

basedir = '/home/tcarrasco/result/data/CR2MET/nday/daily_spamax/'

df = pd.DataFrame(columns=['date', 'lat', 'lon'])

for i in range(1980, 2024):

    filename = f'CR2MET_tmax_v2.5_DJF_1day_{i}_005deg.nc'
    filepath = basedir + filename
    tmax = xr.open_dataset(filepath)['tmax']
    k = tmax.argmax()
    argmax = tmax[k].time
    yy = argmax.dt.year.values
    mm = argmax.dt.month.values
    dd = argmax.dt.day.values
    strdate = f'{yy}-{mm}-{dd}'
    df.loc[i, 'date'] = strdate
print(df)
