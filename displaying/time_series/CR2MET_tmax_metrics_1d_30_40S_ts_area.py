import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.ticker import FormatStrFormatter

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

import utilities.cr2met as cr2met  # noqa: E402

tmax = cr2met.tmax_1d_djf_30_40S().sel(time=slice('1980', '2023'))
tmax_3d = cr2met.tmax_3d_djf_30_40S().sel(time=slice('1980', '2023'))
area_mi = cr2met.area_tmax_1d_30_40S(35).sel(time=slice('1980', '2023'))*1e-3
area_hi = cr2met.area_tmax_1d_30_40S(37).sel(time=slice('1980', '2023'))*1e-3
area_ex = cr2met.area_tmax_1d_30_40S(40).sel(time=slice('1980', '2023'))*1e-3
ndays_hi = cr2met.nday_djf(threshold=37.0).sel(
    time=slice('1980', '2023'))/90*100

boxplot = cr2met.boxplot_tmax_1d_djf_30_40S()
years = np.arange(1980, 2023+1)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
# plt.rcParams['axes.spines.top'] = False
# plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(2, 1, figsize=(8, 4))

axs[0].plot(tmax.time.dt.year, tmax.values, c='#087E8B', lw=1)
axs[0].scatter(tmax.time.dt.year, tmax.values, c='#087E8B', s=30)

axs[1].bar(area_mi.time.dt.year, area_mi.values, color='gray', width=0.6)
axs[1].bar(area_hi.time.dt.year, area_hi.values,
           color='#3E54AC', width=0.6)
axs[1].bar(area_ex.time.dt.year, area_ex.values,
           color='#FC2947', width=0.6)

# axs[0].legend(['Highest Tx [DJF, Chile 30-40ºS]'], loc='upper left',
#               facecolor='white', framealpha=1)
axs[1].legend(['Area Tx > 35ºC', 'Area Tx > 37ºC',
              'Area Tx > 40ºC'], loc='upper center', ncol=3,
              facecolor='white', framealpha=1)

axs[0].set_ylabel('Highest Tx (ºC)')
axs[0].set_ylim([34, 44])
axs[0].set_yticks([34, 36, 38, 40, 42, 44])
axs[1].set_ylabel('Area (1E3 km2)')
axs[1].set_yticks([0, 20, 40, 60, 80])

for ax in axs:
    ax.set_xlim([1979, 2024])
    ax.grid(c='grey', lw=0.5, ls='--', zorder=-4)
    ax.set_axisbelow(True)
    ax.set_xlabel('')

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_metrics_ts_area.png'
plt.savefig(basedir + filename, dpi=300)
plt.show()
