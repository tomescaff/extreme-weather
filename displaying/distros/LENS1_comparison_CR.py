import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum
from scipy.stats import norm
from scipy.stats import kstest

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics, lens, gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402

# gev
tl = lens.lens1_tmax_1d_djf_30_40S_cr()
fit_gev = gev.fit(tl.values)
mu_gev = gev.mean(*fit_gev)

# norm
fit_nor = norm.fit(tl.values)
mu_norm = fit_nor[0]

mu_clim = tl.rolling(time=30, center=True).mean('time')

##
fit_gev = gev.fit(tl.values - mu_gev)
fit_nor = norm.fit(tl.values - mu_norm)

##
n = 1e5
q = np.arange(1, n+1)/(n+1)
x_gev = gev.ppf(q, *fit_gev)
y_nor = norm.ppf(q, *fit_nor)

##
y_rp = np.linspace(-20, 20, 1000)
x_rp = 1/norm.sf(y_rp, *fit_nor)

# computing y values
y_rp_gev = gev.isf(1/x_rp, *fit_gev)
y_rp_nor = norm.isf(1/x_rp, *fit_nor)


# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(1, 3, figsize=(14, 4))

ax = axs[0]
years = tl.time.dt.year
ax.plot(years, tl.values, c='k', lw=0.8, alpha=0.5)
ax.plot(years, np.tile(mu_gev, tl.size), c='#FC2947', lw=0.8)
ax.plot(years, np.tile(mu_norm, tl.size), c='#0B2447', lw=0.8, ls='--')
ax.plot(mu_clim.time.dt.year, mu_clim.values, c='#159895', lw=0.8)
ax.legend(['Ensemble', 'GEV fit', 'Normal fit', '30yr mean'])
ax.grid(c='grey', lw=0.5, ls='--', zorder=-4)
ax.set_axisbelow(True)
ax.set_ylabel('Tmax (ºC)')
ax.set_title('Distribution mean value')

ax = axs[1]
ax.plot([-15, 15], [-15, 15], c='#FC2947')
ax.grid(lw=0.5, ls='--', color='grey')
ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
ax.set_aspect('equal', 'box')
ax.set_title('q-q plot GEV fit vs. Normal fit')
ax.set_xlabel('GEV')
ax.set_ylabel('Normal')
ax.scatter(x_gev, y_nor, ec='k', fc='#159895', s=20, alpha=0.5)

ax = axs[2]
xticks = np.arange(1, 11, 1)
xticks = np.append(xticks, [xticks*z for z in [1e2, 1e3, 1e4]])
ax.grid(lw=0.2, ls='--', c='grey')
ax.set_xscale('log')
ax.set_xticks(xticks)
ax.set_xlim([10, 60000])
ax.set_ylim([-1, 1])
ax.set_title('Return period Normal - GEV')
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Tmax (ºC)')
# ax.plot(x_rp, y_rp_nor, color='#0B2447', lw=1.5, alpha=1, label='Normal')
# ax.plot(x_rp, y_rp_gev, color='#FC2947', lw=1.5, alpha=1, label='GEV')
ax.plot(x_rp, y_rp_nor - y_rp_gev, color='#159895', lw=1.5)
# ax.legend()
plt.tight_layout()

basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_comparison_CR.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
