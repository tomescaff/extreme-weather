import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import sys
import cmaps

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing')  # noqa: E402

import utilities.qgdynamics as qg

basedir = '/home/tcarrasco/result/data/ERA5/uvT/'
filename = 'uvT.nc'

ds = xr.open_dataset(basedir+filename).sel(time='2017')
ua = ds['u'].sel(latitude=-36, longitude=-72)
va = ds['v'].sel(latitude=-36, longitude=-72)
ta = ds['t'].sel(latitude=-36, longitude=-72)

basedir = '/home/tcarrasco/result/data/ERA5/omega/'
filename = 'omega_box.nc'

ds = xr.open_dataset(basedir+filename).sel(time='2017')
om = ds['w'].sel(latitude=-36, longitude=(-72+360) % 360)

plev = ds.level.values
time = ds.time
nlev = plev.size
ntime = time.size
data_ua = np.transpose(ua.values)
data_va = np.transpose(va.values)

theta = ta*(1000/np.tile(np.reshape(plev, (1, 32)), (236, 1))) ** 0.286
data_th = np.transpose(theta.values)

data_om = np.transpose(om.values)

lticks = np.array([1000, 925, 850, 700, 500, 300])
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

levels = np.arange(-27.5, 32.5, 5)

fig, axs = plt.subplots(2, 1, figsize=(12, 8))
plt.sca(axs[0])
cf = plt.contourf(
    x, z, data_ua,
    levels=levels,
    cmap=cmaps.BlueWhiteOrangeRed, extend='both')

cs = plt.contour(x, z, data_th, levels=np.arange(280, 430, 10), colors='k',
                 linewidths=0.5)
plt.clabel(cs, cs.levels, inline=False, fontsize=6)
cbar = plt.colorbar(cf, aspect=40, pad=0.03)
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks(levels)

plt.yticks(hticks, lticks)
xticks = x[::8]
xlabels = [f'2017-{t.dt.month.values:02}-{t.dt.day.values:02}'
           for t in time[::8]]
plt.xticks(xticks, xlabels, rotation=90)
plt.ylabel('Pressure level (hPa)')
plt.title('Zonal wind (colors in m/s) & potential temp.' +
          ' (contours in K) at (-36ºS, -72ºW)')
plt.ylim([hticks[0], hticks[-1]])
plt.grid(which='major', axis='y', linestyle='--', color='grey', lw=0.4)

plt.sca(axs[1])
cf = plt.contourf(
    x, z, data_va,
    levels=levels,
    cmap=cmaps.BlueWhiteOrangeRed, extend='both')
cs = plt.contour(x, z, data_om,
                 levels=[-1.2, -0.9, -0.6, -0.3, 0.3, 0.6, 0.9, 1.2],
                 colors='k',
                 linewidths=0.5)
plt.clabel(cs, cs.levels, inline=False, fontsize=6)
cbar = plt.colorbar(cf, aspect=40, pad=0.03)
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks(levels)
plt.yticks(hticks, lticks)
xticks = x[::8]
xlabels = [f'2017-{t.dt.month.values:02}-{t.dt.day.values:02}'
           for t in time[::8]]
plt.xticks(xticks, xlabels, rotation=90)
plt.ylabel('Pressure level (hPa)')
plt.title('Meridional wind (colors in m/s) & omega' +
          ' (contours in Pa/s) at (-36ºS, -72ºW)')
plt.ylim([hticks[0], hticks[-1]])
plt.tight_layout()
plt.grid(which='major', axis='y', linestyle='--', color='grey', lw=0.4)

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_va_vertical_profile_2017.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
