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


x, y = metrics.lens1_data_tmax_1d()
tg = gmst.annual_lens1_ensmean()
# gev
# init_params = [36.8, 1.3, 1.1, 0.1]
# mu0, sigma, alpha, eta = pmath.mle_gev_2d(y, x, init_params)
# print(mu0, sigma, alpha, eta)
mu0 = 36.84408841810675
sigma = 1.3176836243310976
alpha = 1.1486964600845266
eta = 0.18841727839206607
mu_gev = gev.mean(eta, mu0 + alpha*tg, sigma)

# norm
# init_params = [36.8, 1.3, 1.1]
# mu0, sigma, alpha = pmath.mle_norm_2d(y, x, init_params)
# print(mu0, sigma, alpha)
mu0 = 37.40034726397229
sigma = 1.3804022747353284
alpha = 1.1401555191916812
mu_norm = mu0 + alpha*tg

tlocal = lens.lens1_tmax_1d_djf_30_40S_40m()
mu_ens = tlocal.mean('ensemble')
mu_clim = tlocal.mean('ensemble').rolling(time=30, center=True).mean('time')

##
gev_mean = gev.mean(eta, mu0 + alpha*x, sigma)
nor_mean = mu0 + alpha*x
fit_gev = gev.fit(y - gev_mean)
fit_nor = norm.fit(y - nor_mean)

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
ax.plot(tg.time.dt.year, mu_norm.values, c='#0B2447', lw=0.8, ls='--')
ax.plot(tg.time.dt.year, mu_gev, c='#FC2947', lw=0.8)
ax.plot(mu_ens.time.dt.year, mu_ens.values, c='k', lw=0.8)
ax.plot(mu_clim.time.dt.year, mu_clim.values, c='#159895', lw=0.8)
ax.legend(['Normal fit', 'GEV fit', 'Ensemble mean', '30yr mean'])
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
ax.set_ylim([0, 1])
ax.set_title('Return period Normal - GEV')
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Tmax (ºC)')
# ax.plot(x_rp, y_rp_nor, color='#0B2447', lw=1.5, alpha=1, label='Normal')
# ax.plot(x_rp, y_rp_gev, color='#FC2947', lw=1.5, alpha=1, label='GEV')
ax.plot(x_rp, y_rp_nor - y_rp_gev, color='#159895', lw=1.5)
# ax.legend()
plt.tight_layout()

basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_comparison_40m.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
