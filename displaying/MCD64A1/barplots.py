import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import modis  # noqa: E402

ba_2017 = modis.burned_area_2017()
ba_2017_lm = modis.burned_area_2017_las_maquinas()
ba_2017_cc = modis.burned_area_2017_complejo_concepcion()

ba_2023 = modis.burned_area_2023()
ba_2023_cn = modis.burned_area_2023_complejo_nahuelbuta()
ba_2023_cc = modis.burned_area_2023_complejo_concepcion()

# acc

aba_2017 = modis.acc_burned_area(ba_2017)
aba_2023 = modis.acc_burned_area(ba_2023)

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

plt.sca(axs[0, 1])
plt.bar(time_2023, ba_2023, label='Complejo Nahuelbuta')
plt.bar(time_2023, ba_2023 - ba_2023_cn, label='Complejo Concepción')
plt.bar(time_2023, ba_2023 - ba_2023_cn - ba_2023_cc, label='Other')
plt.xticks(rotation=90)
plt.ylabel('MCD64A1 daily burned area (1E3 Ha)')
plt.legend()

plt.sca(axs[1, 0])
plt.bar(time_2017, aba_2017)  # , label='Las Máquinas')
# plt.bar(time_2017, ba_2017 - ba_2017_lm, label='Complejo Concepción')
# plt.bar(time_2017, ba_2017 - ba_2017_lm - ba_2017_cc, label='Other')
plt.xticks(rotation=90)
plt.ylabel('MCD64A1 acc burned area (1E3 Ha)')
plt.legend()

plt.sca(axs[1, 1])
plt.bar(time_2023, aba_2023)
plt.xticks(rotation=90)
plt.ylabel('MCD64A1 acc burned area (1E3 Ha)')
plt.legend()


plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'MCD64A1_barplot_all.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
