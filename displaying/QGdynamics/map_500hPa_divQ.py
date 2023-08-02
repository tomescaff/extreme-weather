import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.font_manager as font_manager
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.io.shapereader import Reader

import sys
import cmaps

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing')  # noqa: E402

import utilities.qgdynamics as qg

basedir = '/home/tcarrasco/result/data/ERA5/QGDynamic/'
filename = 'ERA5_26Jan2017_700_400.nc'

qvector = qg.qvector(basedir+filename, levi=500)
Q1, Q2, dQ, elon, elat, x, y, ug, vg, u, v, z = qvector


# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 8

fig = plt.figure(figsize=(8, 7))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-80, -60, -60, -10], crs=ccrs.PlateCarree())

# define and set  x and y ticks
xticks = np.arange(-80, -60+10, 10)
yticks = np.arange(-60, -10+10, 10)
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

ax.pcolormesh(x, y, dQ, cmap=cmaps.BlueWhiteOrangeRed, vmin=-0.3, vmax=0.3)
ax.contour(x, y, z, levels=30, linewidths=0.5, colors='k')
del_val = 10
ax.barbs(x[::del_val, ::del_val], y[::del_val, ::del_val],
         Q1[::del_val, ::del_val], Q2[::del_val, ::del_val],
         color='k', pivot='middle', length=4)
plt.title('Z500, Qvec, divQ')

# draw the coastlines
resol = '50m'
land = cfeature.NaturalEarthFeature(
    'physical', 'land',  scale=resol, edgecolor='k', facecolor='none')
ax.add_feature(land, linewidth=0.5, alpha=1, zorder=5)

#  reduce outline patch linewidths
ax.spines['geo'].set_linewidth(0.4)

basedir = '/home/tcarrasco/result/images/png/'
filename = 'QG_divQ.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
