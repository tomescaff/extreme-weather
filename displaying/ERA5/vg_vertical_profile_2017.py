import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import sys
import cmaps

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing')  # noqa: E402

import utilities.qgdynamics as qg

basedir = '/home/tcarrasco/result/data/ERA5/geopotential/'
filename = 'z_box.nc'

ds = qg.geostrophic_wind(basedir+filename).sel(time='2017')
ug = ds['ug'].sel(lat=-36, lon=288)
vg = ds['vg'].sel(lat=-36, lon=288)

plev = ds.level.values
time = ds.time
nlev = plev.size
ntime = time.size
data_ug = np.transpose(ug.values)
data_vg = np.transpose(vg.values)

lticks = np.array([1000, 925, 850, 500, 300])
hticks = 7000*np.log(1000/lticks)
z = 7000*np.log(1000/plev)
x = np.arange(ntime)
# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
fig = plt.figure(figsize=(12, 8))
plt.contourf(
    x, z, data_vg, levels=[-25, -15, -5, 5, 15, 25],
    cmap=cmaps.BlueWhiteOrangeRed)
cs = plt.contour(x, z, data_ug, levels=[-25, -15, -5, 5, 15, 25], colors='k',
                 linewidths=0.8)
plt.yticks(hticks, lticks)
xticks = x[::8]
xlabels = [f'2017-{t.dt.month.values:02}-{t.dt.day.values:02}'
           for t in time[::8]]
plt.xticks(xticks, xlabels, rotation=90)
plt.ylabel('Pressure level (hPa)')
plt.clabel(cs, cs.levels, inline=True, fontsize=8)
plt.title('Potential temperature (K) at (-36ºS, -72ºW)')
plt.ylim([hticks[0], hticks[-1]])

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_vg_vertical_profile_2017.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
