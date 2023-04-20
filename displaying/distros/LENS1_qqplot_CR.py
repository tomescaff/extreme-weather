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
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402


tlocal = lens.lens1_tmax_1d_djf_30_40S_cr()
data = np.ravel(tlocal.values)

fit_nor = norm.fit(data)
fit_gev = gev.fit(data)
fit_gum = gum.fit(data)

n = data.size
x = np.sort(data)
q = (np.arange(1, n+1)/(n+1))

y_nor = norm.ppf(q, *fit_nor)
y_gev = gev.ppf(q, *fit_gev)
y_gum = gum.ppf(q, *fit_gum)

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
fig, axs = plt.subplots(1, 3, figsize=(12, 6))

titles = [x + ' q-q plot' for x in ['Normal', 'GEV', 'Gumbel']]
for ax, title in zip(axs, titles):
    ax.plot([30, 50], [30, 50], c='#FC2947')
    ax.grid(lw=0.2, ls='--', color='grey')
    ax.set_xlim([30, 50])
    ax.set_ylim([30, 50])
    ax.set_aspect('equal', 'box')
    ax.set_title(title)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Reference')

axs[0].scatter(x, y_nor, ec='k', fc='#159895', s=20, alpha=0.5, label='Normal')
axs[1].scatter(x, y_gev, ec='k', fc='#159895', s=20, alpha=0.5, label='GEV')
axs[2].scatter(x, y_gum, ec='k', fc='#159895', s=20, alpha=0.5, label='Gumbel')


plt.tight_layout()
# set title and labels
basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_CR_qqplot.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
