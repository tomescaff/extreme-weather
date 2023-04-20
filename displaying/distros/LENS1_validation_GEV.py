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

xmin, xmax = 30, 45

# axs 0: tlocal
tl = lens.lens1_tmax_1d_djf_30_40S_cr()
data = np.ravel(tl.values)
fit_gev = gev.fit(data)
mu_gev = gev.mean(*fit_gev)
mu_clim = tl.rolling(time=30, center=True).mean('time')

# axs 1: distro
hist, bins = np.histogram(data, bins=np.linspace(30, 50, 80), density=True)

# axs 2: q-q plot
n = data.size
q = np.arange(1, n+1)/(n+1)
x_qq = np.sort(data)
y_gev = gev.ppf(q, *fit_gev)

# ax 3: return period
y_rp = np.linspace(xmin, xmax, 1000)
x_rp = 1/gev.sf(y_rp, *fit_gev)
y_rp_gev = gev.isf(1/x_rp, *fit_gev)
u, tau = pmath.return_periods(data, method='up')  # compute non parametric tau

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(2, 2, figsize=(14, 7.5))
ax = axs[0, 0]
years = tl.time.dt.year
ax.plot(years, tl.values, c='k', lw=0.8, alpha=0.5)
ax.plot(years, np.tile(np.mean(data), tl.size), c='#0B2447', lw=0.8)
ax.plot(years, np.tile(mu_gev, tl.size), c='#FC2947', ls='--', lw=0.8)
ax.plot(mu_clim.time.dt.year, mu_clim.values, c='#159895', lw=0.8)
ax.legend(['CR', 'CR mean', 'GEV fit mean', '30yr mean'], ncol=4, loc=2)
ax.grid(c='grey', lw=0.5, ls='--', zorder=-4)
ax.set_axisbelow(True)
ax.set_ylabel('Tmax (ºC)')
ax.set_title('CESM1-LENS control run')
ax.set_ylim([xmin, xmax])

ax = axs[0, 1]
width = 0.85 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
ax.bar(center, hist, align='center', width=width, edgecolor='#000000',
       facecolor='#65647C', alpha=0.7, lw=0.2, label='CR')
ax.set_xlim([xmin, xmax])
x = np.linspace(xmin, xmax, 100)
ax.plot(x, gev.pdf(x, *fit_gev), c='#FC2947', linewidth=2, label='GEV fit')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend()
ax.set_xlabel('Tmax (ºC)')
ax.set_ylabel('PDF')
ax.set_title('Probability distribution')

ax = axs[1, 0]
ax.plot([xmin, xmax], [xmin, xmax], c='#FC2947')
ax.grid(lw=0.5, ls='--', color='grey')
ax.set_xlim([xmin, xmax])
ax.set_ylim([xmin, xmax])
# ax.set_aspect('equal', 'box')
ax.set_title('Q-Q plot')
ax.set_xlabel('Sample (CR)')
ax.set_ylabel('Reference (GEV fit)')
ax.scatter(x_qq, y_gev, ec='k', fc='#159895', s=20, alpha=0.5)

ax = axs[1, 1]
xticks = np.arange(1, 11, 1)
xticks = np.append(xticks, [xticks*z for z in [1e2, 1e3, 1e4]])
ax.grid(lw=0.2, ls='--', c='grey')
ax.set_xscale('log')
ax.set_xticks(xticks)
ax.set_xlim([0.9, 60000])
ax.set_ylim([30, 50])
ax.set_title('Return periods')
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Tmax (ºC)')
ax.scatter(tau, u, marker='o', facecolor='#65647C',
           edgecolor='#000000', alpha=0.7, label='CR')
ax.plot(x_rp, y_rp_gev, color='#FC2947', lw=1.5, label='GEV fit')
ax.legend()


plt.tight_layout()

basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_validation_GEV.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
plt.show()
