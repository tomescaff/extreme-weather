import cmaps
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


def plev_to_std_height(plev):
    return 7000*np.log(1000/plev)


basedir = '/home/tcarrasco/result/data/ERA5/uvT/'
filename17 = 'perfil_lon_2017.nc'
filename23 = 'perfil_lon_2023.nc'

ds17 = xr.open_dataset(basedir+filename17).squeeze()
ds23 = xr.open_dataset(basedir+filename23).squeeze()

w17 = ds17['w']
u17 = ds17['u']
v17 = ds17['v']
t17 = ds17['t']

w23 = ds23['w']
u23 = ds23['u']
v23 = ds23['v']
t23 = ds23['t']


plev = ds17.level.values
lon = ds17.longitude.values

data_w17 = np.transpose(w17.values)
data_w23 = np.transpose(w23.values)

lticks = np.array([1000, 925, 850, 700, 500, 300])
hticks = 7000*np.log(1000/lticks)
z = plev_to_std_height(plev)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10

levels_w = np.arange(-3.25, 3.25+0.5, 0.5)
levels_u = np.arange(-13, 13+2, 2)

fig, axs = plt.subplots(2, 1, figsize=(12, 8))
plt.sca(axs[0])
cf = plt.contourf(
    lon, z, u17,
    levels=levels_u,
    cmap=cmaps.BlueWhiteOrangeRed, extend='both')
cs = plt.contour(lon, z, w17, colors='k', levels=levels_w,
                 linewidths=0.8)
plt.clabel(cs, cs.levels, inline=True, fontsize=8)
cbar = plt.colorbar(cf, aspect=40, pad=0.03)
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks(levels_u)
plt.yticks(hticks, lticks)
plt.ylabel('Pressure level (hPa)')
plt.title('Omega (colors in Pa/s) & meridional wind' +
          ' (contours in m/s) at 36.5ºS, 2017-01-26 12:00')
plt.ylim([hticks[0], hticks[-1]])
plt.grid(which='major', linestyle='--', color='grey', lw=0.4)

plt.sca(axs[1])
cf = plt.contourf(
    lon, z, u23,
    levels=levels_u,
    cmap=cmaps.BlueWhiteOrangeRed, extend='both')
cs = plt.contour(lon, z, w23, colors='k', levels=levels_w,
                 linewidths=0.8)
plt.clabel(cs, cs.levels, inline=True, fontsize=8)
cbar = plt.colorbar(cf, aspect=40, pad=0.03)
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks(levels_u)
plt.yticks(hticks, lticks)
plt.ylabel('Pressure level (hPa)')
plt.title('Omega (colors in Pa/s) & meridional wind' +
          ' (contours in m/s) at 36.5ºS, 2023-02-03 12:00')
plt.ylim([hticks[0], hticks[-1]])
plt.grid(which='major', linestyle='--', color='grey', lw=0.4)

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_lon_profile_omega.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
