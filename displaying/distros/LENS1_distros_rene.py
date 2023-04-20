import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum
from scipy.stats import norm
from scipy.stats import kstest

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import lens  # noqa: E402
from utilities import metrics  # noqa: E402
from utilities import math as pmath  # noqa: E402

tl = lens.lens1_tmax_1d_djf_30_40S_40m()

tl_pa = np.ravel(tl.sel(time=slice('1921', '1930')).values)
tl_ac = np.ravel(tl.sel(time=slice('2011', '2020')).values)
tl_fu = np.ravel(tl.sel(time=slice('2033', '2052')).values)

# compute histogram
hist_pa, bins_pa = np.histogram(
    tl_pa, bins=np.linspace(30, 50, 80), density=True)
hist_ac, bins_ac = np.histogram(
    tl_ac, bins=np.linspace(30, 50, 80), density=True)
hist_fu, bins_fu = np.histogram(
    tl_fu, bins=np.linspace(30, 50, 80), density=True)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# create figure
fig, axs = plt.subplots(3, 1, figsize=(8, 6))

# plot the histogram
width = 0.85 * (bins_pa[1] - bins_pa[0])
center = (bins_pa[:-1] + bins_pa[1:]) / 2
axs[0].bar(center, hist_pa, align='center', width=width, edgecolor='k',
           facecolor='b', alpha=0.7, lw=0.2, label='LENS1 1921-1930')
width = 0.85 * (bins_ac[1] - bins_ac[0])
center = (bins_ac[:-1] + bins_ac[1:]) / 2
axs[1].bar(center, hist_ac, align='center', width=width, edgecolor='k',
           facecolor='#65647C', alpha=0.7, lw=0.2, label='LENS1 2011-2020')
width = 0.85 * (bins_fu[1] - bins_fu[0])
center = (bins_fu[:-1] + bins_fu[1:]) / 2
axs[2].bar(center, hist_fu, align='center', width=width, edgecolor='k',
           facecolor='r', alpha=0.7, lw=0.2, label='LENS1 2033-2052')


for ax in axs:
    plt.sca(ax)
    plt.xlim([30, 50])
    plt.grid(lw=0.2, ls='--', color='grey')
    plt.legend()
    plt.xlabel('Tmax (ºC)')
    plt.ylabel('PDF')

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_distros_rene.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
