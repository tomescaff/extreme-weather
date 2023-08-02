import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

basedir = '/home/tcarrasco/result/data/FIRMS/tables/'

df17 = pd.read_csv(basedir + 'FIRMS_2017.csv')
df17_lm = pd.read_csv(basedir + 'FIRMS_2017_lm.csv')
df17_co = pd.read_csv(basedir + 'FIRMS_2017_conce.csv')
df23 = pd.read_csv(basedir + 'FIRMS_2023.csv')

area17 = df17['burned_area']*1e-6
time17 = df17['time']
area23 = df23['burned_area']*1e-6
time23 = df23['time']

area17_lm = df17_lm['burned_area']*1e-6
time17_lm = df17_lm['time']
area17_co = df17_co['burned_area']*1e-6
time17_co = df17_co['time']

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 8
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

area_otro = area17 - area17_lm - area17_co

fig, axs = plt.subplots(2, 1, figsize=(8, 8))
plt.sca(axs[0])
plt.bar(time17, area_otro + area17_co + area17_lm)
plt.bar(time17, area_otro + area17_co)  # , bottom=(area17-area17_lm))
plt.bar(time17, area_otro)
plt.xticks(rotation=90)
plt.ylabel('FIRMS area burnt (km2)')

plt.sca(axs[1])
plt.bar(time23, area23)
plt.xticks(rotation=90)
plt.ylabel('FIRMS area burnt (km2)')

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'FIRMS_barplot.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
