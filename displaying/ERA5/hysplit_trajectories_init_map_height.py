import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from glob import glob

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.io.shapereader import Reader

year = 2017
basedir = '/home/tcarrasco/result/data/HYSPLIT/traj_init/traj_' + str(year)
filepaths = glob(basedir + '/*.txt')

lats = []
lons = []
indices = []
height = []
for i, filepath in enumerate(filepaths):
    df = pd.read_csv(filepath, skiprows=20, header=None, sep='\s+')  # noqa: W605
    lat = df.loc[df[8] == -24, 9].values
    lon = df.loc[df[8] == -24, 10].values
    h = df.loc[df[8] == -24, 11].values
    index = np.ones(lon.shape)*(-6*(8-i))
    lats = lats + lat.tolist()
    lons = lons + lon.tolist()
    indices = indices + index.tolist()
    height = height + h.tolist()

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 8

fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
latmin, latmax, dlat = -50, -30, 5
lonmin, lonmax, dlon = -90, -60, 10
ax.set_extent([lonmin, lonmax, latmin, latmax], crs=ccrs.PlateCarree())

# define and set  x and y ticks
xticks = np.arange(lonmin, lonmax+dlon, dlon)
yticks = np.arange(latmin, latmax+dlat, dlat)
ax.set_xticks(xticks, crs=ccrs.PlateCarree())
ax.set_yticks(yticks, crs=ccrs.PlateCarree())

# format x and y labels
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

# add grid using previous ticks
gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.5,
                  color='grey', alpha=0.7, linestyle='--', draw_labels=False)
gl.xlocator = mticker.FixedLocator(xticks)
gl.ylocator = mticker.FixedLocator(yticks)

sc = ax.scatter(lons, lats, s=20, edgecolor='k',
                c=height, alpha=0.7, cmap='jet')
cbar = plt.colorbar(sc, aspect=40, pad=0.03)
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks(np.arange(0, 4500, 100))

# draw the coastlines
resol = '50m'
land = cfeature.NaturalEarthFeature(
    'physical', 'land',  scale=resol, edgecolor='k', facecolor='none')
ax.add_feature(land, linewidth=0.5, alpha=1, zorder=5)

fname = '/home/tcarrasco/result/data/shp/Regiones/Regional.shp'

ax.add_geometries(Reader(fname).geometries(), ccrs.Mercator.GOOGLE,
                  facecolor='none', edgecolor='k', zorder=6, lw=0.4)

#  reduce outline patch linewidths
ax.spines['geo'].set_linewidth(0.4)

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_hysplit_init_'+str(year)+'_height.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
