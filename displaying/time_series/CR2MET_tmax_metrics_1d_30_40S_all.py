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
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(5, 1, figsize=(10, 10))

axs[0].plot(tmax.time.dt.year, tmax.values, c='#087E8B', lw=1)
axs[0].scatter(tmax.time.dt.year, tmax.values, c='#087E8B', s=30)

axs[1].plot(tmax_3d.time.dt.year, tmax_3d.values, c='#3E54AC', lw=1)
axs[1].scatter(tmax_3d.time.dt.year, tmax_3d.values, c='#3E54AC', s=30)

axs[2].boxplot(boxplot, positions=years)
axs[2].set_xticks(np.arange(1980, 2024, 5), [str(x)
                  for x in np.arange(1980, 2024, 5)])

axs[3].plot(ndays_hi.time.dt.year, ndays_hi.values, c='#FF6D60', lw=1)
axs[3].scatter(ndays_hi.time.dt.year, ndays_hi.values, c='#FF6D60', s=30)

axs[4].bar(area_mi.time.dt.year, area_mi.values, color='gray', width=0.25)
axs[4].bar(area_hi.time.dt.year+0.25, area_hi.values,
           color='#3E54AC', width=0.25)
axs[4].bar(area_ex.time.dt.year+0.5, area_ex.values,
           color='#FC2947', width=0.25)

axs[0].legend(['Highest Tx [DJF, 30-40ºS]'], loc='upper left')
axs[1].legend(['Highest 3-day averaged Tx [DJF, 30-40ºS]'], loc='upper left')
axs[2].legend(['Highest Tx [30-40ºS]'], loc='upper left')
axs[3].legend(['Days Tx [30-40ºS] > 37ºC '], loc='upper left')
axs[4].legend(['Area Tx [DJF] > 35ºC', 'Area Tx [DJF] > 37ºC',
              'Area Tx [DJF] > 40ºC'], loc='upper left', ncol=3)

axs[0].set_ylabel('Temperature (ºC)')
axs[0].set_ylim([35, 43])
axs[0].set_yticks([36, 38, 40, 42])
axs[1].set_ylabel('Temperature (ºC)')
axs[1].set_ylim([33, 41])
axs[1].set_yticks([34, 36, 38, 40])
axs[2].set_ylabel('Temperature (ºC)')
axs[2].set_ylim([20, 48])
axs[3].set_ylabel('Days of summer (%)')
axs[4].set_ylabel('Area (1E3 km2)')

for ax in axs:
    ax.set_xlim([1979, 2024])
    ax.grid(c='grey', lw=0.5, ls='--', zorder=-4)
    ax.set_axisbelow(True)
    ax.set_xlabel('')

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_metrics_all_boxplot.png'
plt.savefig(basedir + filename, dpi=300)
plt.show()
