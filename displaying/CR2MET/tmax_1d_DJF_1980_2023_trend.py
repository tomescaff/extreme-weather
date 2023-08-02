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
import xarray as xr
import numpy as np

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing')  # noqa: E402

import utilities.cr2met as cr2met

filepath = '/home/tcarrasco/result/data/CR2MET/trend/tmax_1d_djf_trend.nc'

slope = xr.open_dataset(filepath)['slope']*100

mask = cr2met.clmask()

da = slope*mask

pvals = xr.open_dataset(filepath)['pvalue'].values
pmask = pvals  # < 0.01
data = np.where(pmask, da.values, np.nan)

fname = '/home/tcarrasco/result/data/shp/Regiones/Regional.shp'

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 8

# create figure
fig = plt.figure(figsize=(8, 7))

# define projection
ax = plt.axes(projection=ccrs.PlateCarree())

# set extent of map
ax.set_extent([-76, -66.5, -56.5, -17], crs=ccrs.PlateCarree())

# define and set  x and y ticks
xticks = [-76, -72, -68]
yticks = [-55, -50, -45, -40, -35, -30, -25, -20]
ax.set_xticks(xticks, crs=ccrs.PlateCarree())
ax.set_yticks(yticks, crs=ccrs.PlateCarree())

# format x and y labels
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

# add backgroung for land and ocean
resol = '50m'
land = cfeature.NaturalEarthFeature(
    'physical', 'land',  scale=resol, edgecolor='k',
    facecolor=cfeature.COLORS['land'])
ocean = cfeature.NaturalEarthFeature(
    'physical', 'ocean', scale=resol, edgecolor='none',
    facecolor=cfeature.COLORS['water'])

ax.add_feature(land, linewidth=0.0, alpha=0.5)
ax.add_feature(ocean, alpha=0.5)

# add grid using previous ticks
gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.5,
                  color='grey', alpha=0.7, linestyle='--', draw_labels=False)
gl.xlocator = mticker.FixedLocator(xticks)
gl.ylocator = mticker.FixedLocator(yticks)

# plot the climatology and reshape color bar
pcm = ax.pcolormesh(da.lon.values, da.lat.values, data,
                    cmap=cmaps.temp_diff_18lev, zorder=4, vmin=-12, vmax=12)
cbar = plt.colorbar(pcm, aspect=40, pad=0.03)

density = 7
ax.contourf(da.lon.values, da.lat.values, pvals*mask,
            transform=ccrs.PlateCarree(), colors='none', levels=[.0, 0.01],
            hatches=[density*'/', density*'/'], zorder=5,
            )

# draw the coastlines
land = cfeature.NaturalEarthFeature(
    'physical', 'land',  scale=resol, edgecolor='k', facecolor='none')
ax.add_feature(land, linewidth=0.5, alpha=1, zorder=6)

ax.add_geometries(Reader(fname).geometries(), ccrs.Mercator.GOOGLE,
                  facecolor='none', edgecolor='k', zorder=7, lw=0.4)

#  reduce outline patch linewidths
cbar.outline.set_linewidth(0.4)
ax.spines['geo'].set_linewidth(0.4)

basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_tmax_1d_DJF_trend_1980_2023.png'
filepath = basedir+filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
