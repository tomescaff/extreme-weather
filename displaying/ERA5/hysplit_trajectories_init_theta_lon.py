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

dth_00_24 = []
dth_24_72 = []
ini_lons = []
ths_00 = []

for i, filepath in enumerate(filepaths):
    df = pd.read_csv(filepath, skiprows=19, header=None, sep='\s+')  # noqa: W605

    for j in range(1, 13):
        df_traj = df.loc[df[0] == j, :]
        th_00 = float(df_traj.loc[df_traj[8] == 0, 13].values)
        th_24 = float(df_traj.loc[df_traj[8] == -24, 13].values)
        th_72 = float(df_traj.loc[df_traj[8] == -72, 13].values)
        ini_lon = float(df_traj.loc[df_traj[8] == -72, 10].values)

        dth_00_24.append(th_00-th_24)
        dth_24_72.append(th_24-th_72)
        ini_lons.append(ini_lon)
        ths_00.append(th_00)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 8

fig, axs = plt.subplots(2, 1, figsize=(8, 8))
plt.sca(axs[0])
sc = plt.scatter(ini_lons, dth_00_24, c=ths_00, cmap='jet',
                 edgecolors='k', vmin=300, vmax=317)
cbar = plt.colorbar(sc, aspect=40, pad=0.03)
cbar.ax.tick_params(labelsize=8)
cbar.ax.set_ylabel('Final potential temperature')
plt.ylim([-30, 30])
plt.xlim([-130, -60])
plt.axhline([0], lw=0.8, c='k')
plt.axvline([-73], lw=0.8, c='k')
plt.xlabel('Initial longitude')
plt.ylabel('0-24 potential temperature change')


plt.sca(axs[1])
sc = plt.scatter(ini_lons, dth_24_72, c=ths_00, cmap='jet',
                 edgecolors='k', vmin=300, vmax=317)
cbar = plt.colorbar(sc, aspect=40, pad=0.03)
cbar.ax.tick_params(labelsize=8)
cbar.ax.set_ylabel('Final potential temperature')
plt.ylim([-30, 30])
plt.xlim([-130, -60])
plt.axhline([0], lw=0.8, c='k')
plt.axvline([-73], lw=0.8, c='k')
plt.xlabel('Initial longitude')
plt.ylabel('24-72 hrs potential temperature change')

plt.tight_layout()

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_hysplit_init_'+str(year)+'_theta_lon.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
