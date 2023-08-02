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

basedir = '/home/tcarrasco/result/data/MODIS/'
filename = 'snapshot-2023-02-03T00_00_00Z_LST.tiff'
filepath = basedir + filename

da = xr.open_rasterio(filepath).transpose('x', 'y', 'band')

# 0 = 200k
# 255 = 350k

# vmin = 260k
# vmax = 330k

# x -> pixel
# y -> kelvin

m = float(350-200)/float(255-0)
b = 200

# y = mx + b
# x = (y-b)/m

vmin = int((260-b)/m)
vmax = int((330-b)/m)


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
crs = ccrs.PlateCarree()
ax = plt.axes(projection=crs)

# set extent of map
ax.set_extent([-75, -69.5, -40, -30], crs=crs)

# define and set  x and y ticks
xticks = [-74, -72, -70]
yticks = [-40, -37.5, -35, -32.5, -30]
ax.set_xticks(xticks, crs=ccrs.PlateCarree())
ax.set_yticks(yticks, crs=ccrs.PlateCarree())

# format x and y labels
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

# add backgroung for land and ocean
resol = '50m'
# land = cfeature.NaturalEarthFeature(
#     'physical', 'land',  scale=resol, edgecolor='k',
#     facecolor=cfeature.COLORS['land'])
# ocean = cfeature.NaturalEarthFeature(
#     'physical', 'ocean', scale=resol, edgecolor='none',
#     facecolor=cfeature.COLORS['water'])

# ax.add_feature(land, linewidth=0.0, alpha=0.5)
# ax.add_feature(ocean, alpha=0.5)

# add grid using previous ticks
gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.5,
                  color='grey', alpha=0.7, linestyle='--', draw_labels=False)
gl.xlocator = mticker.FixedLocator(xticks)
gl.ylocator = mticker.FixedLocator(yticks)

# plot the climatology and reshape color bar
pcm = da.plot.imshow(ax=ax, x='x', y='y', rgb='band', transform=crs,
                     cmap=cmaps.MPL_gist_rainbow_r, zorder=0,
                     vmin=vmin, vmax=vmax)

cbar = plt.colorbar(pcm, aspect=40, pad=0.03)

ax.add_geometries(Reader(fname).geometries(), ccrs.Mercator.GOOGLE,
                  facecolor='none', edgecolor='k', zorder=6, lw=0.4)
ax.set_xlabel('')
ax.set_ylabel('')

# reduce outline patch linewidths
cbar.outline.set_linewidth(0.4)
ax.spines['geo'].set_linewidth(0.4)

basedir = '/home/tcarrasco/result/images/png/'
filename = f'MODIS_maps_2023_LST.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
