import xarray as xr
import numpy as np
import pandas as pd

delta = 0.00439453125
R = 6356.7523*1e3

basedir = '/home/tcarrasco/result/data/MCD64A1/clipped/'
filename = 'MCD64monthly.A2023032.Win07.061.burndate.clip'
filepath = basedir + filename + '.tif'
raster = xr.open_dataset(filepath, engine="rasterio")

data = raster.band_data.squeeze()

lons = raster.x
lats = raster.y

days = np.arange(1, 366)
df = pd.DataFrame(columns=['nday', 'freq', 'area'])
df['nday'] = days
df['freq'] = days*0
df['area'] = days*0

for i in range(lats.size):
    for j in range(lons.size):

        val = data.values[i, j]
        lat = lats.values[i]
        lon = lons.values[j]

        lat_rad = lat*np.pi/180
        R_z = R*np.cos(lat_rad)

        dy = delta*np.pi*R/180
        dx = delta*np.pi*R_z/180

        area = dy*dx

        if ~np.isnan(val) and val > 0:
            df.loc[df['nday'] == val,
                   'freq'] = df.loc[df['nday'] == val, 'freq'] + 1
            df.loc[df['nday'] == val, 'area'] = df.loc[df['nday']
                                                       == val, 'area'] + area


outdir = '/home/tcarrasco/result/data/MCD64A1/tables/'
outname = filename + '.csv'
# filename = 'MCD64monthly.A2017001.Win06.061.burndate.clip.csv'
outpath = outdir + outname
df.to_csv(outpath)
