import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum
from scipy.stats import norm
from scipy.stats import kstest

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402


tg, tl = metrics.lens1_data_tmax_1d()
n = tl.size
q = (np.arange(1, n+1)/(n+1))

# norm
init_params = [36.8, 1.3, 1.1]
mu0, sigma, alpha = pmath.mle_norm_2d(tl, tg, init_params)
mu = mu0 + alpha*tg

z = (tl - mu)/sigma
x_nor = np.sort(z)
y_nor = norm.ppf(q, loc=0, scale=1)

# gev
init_params = [36.8, 1.3, 1.1, 0.1]
mu0, sigma, alpha, eta = pmath.mle_gev_2d(tl, tg, init_params)
mu = mu0 + alpha*tg

z = (1/(-eta))*np.log(1+(-eta)*((tl - mu)/sigma))
x_gev = np.sort(z)
y_gev = -np.log(-np.log(q))

# gumbel
init_params = [36.8, 1.3, 1.1]
mu0, sigma, alpha = pmath.mle_gumbel_2d(tl, tg, init_params)
mu = mu0 + alpha*tg

z = (tl - mu)/sigma
x_gum = np.sort(z)
y_gum = gum.ppf(q, loc=0, scale=1)

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
    ax.plot([-15, 15], [-15, 15], c='#FC2947')
    ax.grid(lw=0.2, ls='--', color='grey')
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.set_aspect('equal', 'box')
    ax.set_title(title)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Reference')

axs[0].scatter(x_nor, y_nor, ec='k', fc='#159895', s=20, alpha=0.5)
axs[1].scatter(x_gev, y_gev, ec='k', fc='#159895', s=20, alpha=0.5)
axs[2].scatter(x_gum, y_gum, ec='k', fc='#159895', s=20, alpha=0.5)

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_40m_transform_qqplot.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
