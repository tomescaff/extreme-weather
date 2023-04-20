import sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.ticker import FormatStrFormatter

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

import utilities.cr2met as cr2met  # noqa: E402

tmax = cr2met.tmax_1d_djf_30_40S()
area_mi = cr2met.area_tmax_1d_30_40S(35)*1e-3
area_hi = cr2met.area_tmax_1d_30_40S(38)*1e-3
area_ex = cr2met.area_tmax_1d_30_40S(40)*1e-3

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(4, 1, figsize=(10, 7.5))


axs[0].plot(tmax.time.dt.year, tmax.values, c='#087E8B', lw=1)
axs[0].scatter(tmax.time.dt.year, tmax.values, c='#087E8B', s=30)
axs[1].bar(area_mi.time.dt.year, area_mi.values, color='#3E54AC')
axs[2].bar(area_hi.time.dt.year, area_hi.values, color='#FC2947')
axs[3].bar(area_ex.time.dt.year, area_ex.values, color='#2D2727')

axs[0].legend(['Tmax (DJF, 30-40ºS)'], loc='upper center')
axs[1].legend(['Area Tmax > 35ºC'], loc='upper center')
axs[2].legend(['Area Tmax > 38ºC'], loc='upper center')
axs[3].legend(['Area Tmax > 40ºC'], loc='upper center')

axs[0].set_ylabel('Temperature (ºC)')
axs[1].set_ylabel('Area (1E3 km2)')
axs[2].set_ylabel('Area (1E3 km2)')
axs[3].set_ylabel('Area (1E3 km2)')

for ax in axs:
    ax.grid(c='grey', lw=0.5, ls='--', zorder=-4)
    ax.set_axisbelow(True)
    ax.set_xlabel('')

plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/CR2MET_metrics.png', dpi=300)
plt.show()
