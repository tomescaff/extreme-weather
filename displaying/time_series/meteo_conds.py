import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import modis, cr2met  # noqa: E402
from utilities import stations as stns  # noqa: E402

ba_2017 = modis.burned_area_2017()
ba_2017_lm = modis.burned_area_2017_las_maquinas()
ba_2017_cc = modis.burned_area_2017_complejo_concepcion()

ba_2023 = modis.burned_area_2023()
ba_2023_cn = modis.burned_area_2023_complejo_nahuelbuta()
ba_2023_cc = modis.burned_area_2023_complejo_concepcion()

cu = stns.cu_tmax_daily_1958_2023()
ch = stns.ch_tmax_daily_1960_2023()
te = stns.te_tmax_daily_1960_2023()
la = stns.la_tmax_daily_1960_2023()

cu_2017 = cu.sel(time=slice('2017-01-01', '2017-02-28'))
ch_2017 = ch.sel(time=slice('2017-01-01', '2017-02-28'))
te_2017 = te.sel(time=slice('2017-01-01', '2017-02-28'))
la_2017 = la.sel(time=slice('2017-01-01', '2017-02-28'))

cu_2023 = cu.sel(time=slice('2023-01-01', '2023-02-28'))
ch_2023 = ch.sel(time=slice('2023-01-01', '2023-02-28'))
te_2023 = te.sel(time=slice('2023-01-01', '2023-02-28'))
la_2023 = la.sel(time=slice('2023-01-01', '2023-02-28'))

cu_2017 = stns.fill_na(cu_2017, '2017-01-01', '2017-02-28')
ch_2017 = stns.fill_na(ch_2017, '2017-01-01', '2017-02-28')
te_2017 = stns.fill_na(te_2017, '2017-01-01', '2017-02-28')
la_2017 = stns.fill_na(la_2017, '2017-01-01', '2017-02-28')

cu_2023 = stns.fill_na(cu_2023, '2023-01-01', '2023-02-28')
ch_2023 = stns.fill_na(ch_2023, '2023-01-01', '2023-02-28')
te_2023 = stns.fill_na(te_2023, '2023-01-01', '2023-02-28')
la_2023 = stns.fill_na(la_2023, '2023-01-01', '2023-02-28')

cu_ene = 30.34
cu_feb = 29.60
cu_enefeb = (cu_ene*31+cu_feb*28)/(31+28)

ch_ene = 29.59
ch_feb = 29.22
ch_enefeb = (ch_ene*31+ch_feb*28)/(31+28)

la_ene = 29.37
la_feb = 28.92
la_enefeb = (la_ene*31+la_feb*28)/(31+28)

te_ene = 24.7
te_feb = 25.61
te_enefeb = (te_ene*31+te_feb*28)/(31+28)


spamax_2017 = cr2met.daily_spamax_djf(year='2017')
spamax_2017 = spamax_2017.sel(time=slice('2017-01-01', '2017-02-28'))

spamax_2023 = cr2met.daily_spamax_djf(year='2023')
spamax_2023 = spamax_2023.sel(time=slice('2023-01-01', '2023-02-28'))

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 8
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# area_otro = area17 - area17_lm - area17_co

time_2017 = ba_2017.time.values
time_2023 = ba_2023.time.values

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
plt.sca(axs[0, 0])
plt.bar(time_2017, ba_2017, label='Las Máquinas')
plt.bar(time_2017, ba_2017 - ba_2017_lm, label='Complejo Concepción')
plt.bar(time_2017, ba_2017 - ba_2017_lm - ba_2017_cc, label='Other')
plt.xticks(rotation=90)
plt.ylabel('MCD64A1 daily burned area (1E3 Ha)')
plt.legend()
plt.ylim([0, 130])
plt.grid(lw=0.3, c='gray', ls='dotted')
plt.xticks(time_2017[::5])

plt.sca(axs[0, 1])
plt.bar(time_2023, ba_2023, label='Complejo Nahuelbuta')
plt.bar(time_2023, ba_2023 - ba_2023_cn, label='Complejo Concepción')
plt.bar(time_2023, ba_2023 - ba_2023_cn - ba_2023_cc, label='Other')
plt.xticks(rotation=90)
plt.ylabel('MCD64A1 daily burned area (1E3 Ha)')
plt.legend()
plt.ylim([0, 130])
plt.grid(lw=0.3, c='gray', ls='dotted')
plt.xticks(time_2023[::5])

plt.sca(axs[1, 0])
plt.plot(time_2017, ch_2017, marker='o', ms=3.8, lw=1.2, c='#D95319')
plt.plot(time_2017, cu_2017, marker='D', ms=3.8, lw=1.2, c='#068FFF')
plt.plot(time_2017, spamax_2017, marker='s', ms=3.8, lw=1.2, c='#86C8BC')
plt.axhline(ch_enefeb, lw=0.8, ls='--', c='#D95319')
plt.axhline(cu_enefeb, lw=0.8, ls='--', c='#068FFF')
plt.xticks(rotation=90)
plt.ylabel('Tx (ºC)')
plt.legend(['Chillán', 'Curicó', 'CR2MET max'])
plt.ylim([20, 43])
plt.grid(lw=0.3, c='gray', ls='dotted')
plt.xticks(time_2017[::5])
plt.yticks(np.arange(20, 45, 2.5))

plt.sca(axs[1, 1])
plt.plot(time_2023, ch_2023, marker='o', ms=3.8, lw=1.2, c='#D95319')
plt.plot(time_2023, la_2023, marker='D', ms=3.8, lw=1.2, c='#4DBEEE')
plt.plot(time_2023, spamax_2023, marker='s', ms=3.8, lw=1.2, c='#86C8BC')
plt.axhline(la_enefeb, lw=0.8, ls='--', c='#068FFF')
plt.axhline(ch_enefeb, lw=0.8, ls='--', c='#D95319')
plt.xticks(rotation=90)
plt.ylabel('Tx (ºC)')
plt.legend(['Chillán', 'Los Ángeles', 'CR2MET max'])
plt.ylim([20, 43])
plt.grid(lw=0.3, c='gray', ls='dotted')
plt.xticks(time_2023[::5])
plt.yticks(np.arange(20, 45, 2.5))


plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'meteo_conds.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
