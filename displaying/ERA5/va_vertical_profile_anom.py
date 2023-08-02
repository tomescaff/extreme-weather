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

um = np.mean(ua.values, axis=1)
vm = np.mean(va.values, axis=1)

ua = ua - np.tile(np.reshape(um, (um.size, 1)), (1, 32))
va = va - np.tile(np.reshape(vm, (vm.size, 1)), (1, 32))

plev = ds.level.values
time = ds.time
nlev = plev.size
ntime = time.size
data_ua = np.transpose(ua.values)
data_va = np.transpose(va.values)

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

levels = np.arange(-27.5, 32.5, 5)/5

fig, axs = plt.subplots(2, 1, figsize=(12, 8))
plt.sca(axs[0])
plt.contourf(
    x, z, data_ua,
    levels=levels,
    cmap=cmaps.BlueWhiteOrangeRed, extend='both')
plt.yticks(hticks, lticks)
xticks = x[::8]
xlabels = [f'2017-{t.dt.month.values:02}-{t.dt.day.values:02}'
           for t in time[::8]]
plt.xticks(xticks, xlabels, rotation=90)
plt.ylabel('Pressure level (hPa)')
plt.title('Zonal wind (m/s) at (-36ºS, -72ºW)')
plt.ylim([hticks[0], hticks[-1]])

plt.sca(axs[1])
plt.contourf(
    x, z, data_va,
    levels=levels,
    cmap=cmaps.BlueWhiteOrangeRed, extend='both')
plt.yticks(hticks, lticks)
xticks = x[::8]
xlabels = [f'2017-{t.dt.month.values:02}-{t.dt.day.values:02}'
           for t in time[::8]]
plt.xticks(xticks, xlabels, rotation=90)
plt.ylabel('Pressure level (hPa)')
plt.title('Meridional wind (m/s) at (-36ºS, -72ºW)')
plt.ylim([hticks[0], hticks[-1]])
plt.tight_layout()

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_va_vertical_profile_2017_anom.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
