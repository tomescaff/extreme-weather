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

# compute non parametric tau
u, tau = pmath.return_periods(data, method='up')

# computing best x ticks
y = np.linspace(30, 50, 1000)
x = 1/norm.sf(y, *fit_nor)

# computing y values
y_norm = norm.isf(1/x, *fit_nor)
y_gev = gev.isf(1/x, *fit_gev)
y_gum = gum.isf(1/x, *fit_gum)


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

xticks = np.arange(1, 11, 1)
xticks = np.append(xticks, [xticks*z for z in [1e2, 1e3, 1e4]])

titles = ['Sample vs. ' + x for x in ['Normal', 'GEV', 'Gumbel']]
for ax, title in zip(axs, titles):
    ax.grid(lw=0.2, ls='--', c='grey')
    ax.set_xscale('log')
    ax.set_xticks(xticks)
    ax.set_xlim([0.9, 60000])
    ax.set_ylim([30, 50])
    ax.set_title(title)
    ax.set_xlabel('Return period (yr)')
    ax.set_ylabel('Tmax (ºC)')
    ax.scatter(tau, u, marker='o', fc='#159895', ec='#000000', alpha=0.7)

# plot the parametric curves
axs[0].plot(x, y_norm, color='#FC2947', lw=1.5, alpha=1)
axs[1].plot(x, y_gev, color='#FC2947', lw=1.5, alpha=1)
axs[2].plot(x, y_gum, color='#FC2947', lw=1.5, alpha=1)

plt.tight_layout()

basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_CR_return_period_3subplots.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
