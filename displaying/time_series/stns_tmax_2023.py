import sys
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

import utilities.stations as stns  # noqa: E402

ch = stns.ch_tmax_daily_1960_2023()
te = stns.te_tmax_daily_1960_2023()
la = stns.la_tmax_daily_1960_2023()

ch = ch.sel(time=slice('2023-01-01', '2023-02-28'))
te = te.sel(time=slice('2023-01-01', '2023-02-28'))
la = la.sel(time=slice('2023-01-01', '2023-02-28'))

tch = stns.tch_wind_2023()

ch_ene = 29.59
ch_feb = 29.22
ch_enefeb = (ch_ene*31+ch_feb*28)/(31+28)

la_ene = 29.37
la_feb = 28.92
la_enefeb = (la_ene*31+la_feb*28)/(31+28)

te_ene = 24.7
te_feb = 25.61
te_enefeb = (te_ene*31+te_feb*28)/(31+28)


def fill_na(data_array):
    dr = pd.date_range('2023-01-01', '2023-02-28', freq='1D')
    da_ans = xr.DataArray(np.zeros((dr.size,))*np.nan,
                          coords=[dr],
                          dims=['time'])
    for i, date in enumerate(dr):
        try:
            da_ans[i] = data_array.sel(time=date)
        except Exception as e:
            continue
    return da_ans


ch = fill_na(ch)
te = fill_na(te)
la = fill_na(la)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams["font.family"] = 'arial'
plt.rcParams["font.size"] = '6'

fig, axs = plt.subplots(6, 1, figsize=(4, 6))

c = '#D95319'
plt.sca(axs[0])
plt.plot(np.arange(ch.time.size), ch.values,
         marker='o', ms=3.8, lw=1.2, c=c, zorder=100)
plt.axhline(ch_enefeb, c=c, lw=0.6, ls='--')
plt.ylim([20, 45])
plt.xlim([-4, 60])
plt.xticks(np.arange(0, 65, 5))
plt.yticks([20, 30, 40])
plt.ylabel('Tx (ºC)')
plt.grid(lw=0.2, c='gray', ls='dotted')
plt.tick_params(axis='x', which='both', bottom=False,
                top=False, labelbottom=False)
axs[0].spines[['left', 'top']].set_visible(False)
axs[0].tick_params(axis="y", direction="in")
axs[0].spines['right'].set_color(c)
axs[0].spines['right'].set_linewidth(0.5)
axs[0].spines['bottom'].set_color('gray')
axs[0].spines['bottom'].set_linewidth(0.1)
axs[0].spines['bottom'].set_linestyle('dotted')
axs[0].tick_params(axis='y', colors=c, width=0.5)
axs[0].yaxis.label.set_color(c)
axs[0].yaxis.tick_right()
axs[0].yaxis.set_label_position("right")


c = '#068FFF'
plt.sca(axs[1])
plt.plot(np.arange(la.time.size), la.values,
         marker='o', ms=3.8, lw=1.2, c=c, zorder=100)
plt.axhline(la_enefeb, c=c, lw=0.6, ls='--')
plt.ylim([20, 45])
plt.xlim([-4, 60])
plt.xticks(np.arange(0, 65, 5))
plt.yticks([20, 30, 40])
plt.ylabel('Tx (ºC)')
plt.grid(lw=0.2, c='gray', ls='dotted')
plt.tick_params(axis='x', which='both', bottom=False,
                top=False, labelbottom=False)
axs[1].spines[['right', 'top']].set_visible(False)
axs[1].tick_params(axis="y", direction="in")
axs[1].spines['left'].set_color(c)
axs[1].spines['left'].set_linewidth(0.5)
axs[1].spines['bottom'].set_color('gray')
axs[1].spines['bottom'].set_linewidth(0.1)
axs[1].spines['bottom'].set_linestyle('dotted')
axs[1].tick_params(axis='y', colors=c, width=0.5)
axs[1].yaxis.label.set_color(c)


c = '#86C8BC'
plt.sca(axs[2])
plt.plot(np.arange(te.time.size), te.values,
         marker='o', ms=3.8, lw=1.2, c=c, zorder=100)
plt.axhline(te_enefeb, c=c, lw=0.6, ls='--')
plt.ylim([15, 45])
plt.xlim([-4, 60])
plt.xticks(np.arange(0, 65, 5))
plt.yticks([20, 30, 40])
plt.ylabel('Tx (ºC)')
plt.grid(lw=0.2, c='gray', ls='dotted')
plt.tick_params(axis='x', which='both', bottom=False,
                top=False, labelbottom=False)
axs[2].spines[['left', 'top', 'bottom']].set_visible(False)
axs[2].tick_params(axis="y", direction="in")
axs[2].spines['right'].set_color(c)
axs[2].spines['right'].set_linewidth(0.5)
axs[2].spines['bottom'].set_color('gray')
axs[2].spines['bottom'].set_linewidth(0.1)
axs[2].spines['bottom'].set_linestyle('dotted')
axs[2].tick_params(axis='y', colors=c, width=0.5)
axs[2].yaxis.label.set_color(c)
axs[2].yaxis.tick_right()
axs[2].yaxis.set_label_position("right")

c = '#4DBEEE'
plt.sca(axs[3])
plt.plot(np.arange(tch.time.size), tch.values,
         marker='o', ms=3.8, lw=1.2, c=c, zorder=100)
plt.ylim([0, 25])
plt.xlim([-4, 60])
plt.xticks(np.arange(0, 65, 5))
plt.yticks([0, 10, 20])
plt.ylabel('Wind speed (Kt)')
plt.grid(lw=0.2, c='gray', ls='dotted')
plt.tick_params(axis='x', which='both', bottom=False,
                top=False, labelbottom=False)
axs[3].spines[['right', 'top']].set_visible(False)
axs[3].tick_params(axis="y", direction="in")
axs[3].spines['left'].set_color(c)
axs[3].spines['left'].set_linewidth(0.5)
axs[3].spines['bottom'].set_color('gray')
axs[3].spines['bottom'].set_linewidth(0.1)
axs[3].spines['bottom'].set_linestyle('dotted')
axs[3].tick_params(axis='y', colors=c, width=0.5)
axs[3].yaxis.label.set_color(c)

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'stns_tmax.png'
plt.savefig(basedir + filename, dpi=300)
# plt.show()
