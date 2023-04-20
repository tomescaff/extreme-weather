import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import norm

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import lens  # noqa: E402
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402

tglobal = gmst.annual_lens1_ensmean()
tlocal = lens.lens1_tmax_1d_djf_30_40S_40m()

tglobal = tglobal.sel(time=slice('1920', '2099'))
tlocal = tlocal.sel(time=slice('1921', '2100'))  # 40 ensemble members

x = np.tile(tglobal.values, tlocal.shape[1])
y = np.ravel(tlocal.values, order='F')

init_params = [36.8, 1.3, 1.1]
mu0, sigma, alpha = pmath.mle_norm_2d(y, x, init_params)

mu = mu0 + alpha*tglobal.values
mean = norm.mean(mu, sigma)
std = norm.std(mu, sigma)
mean_plus_1std = mean + std
mean_plus_2std = mean + 2*std
val_tau_10 = norm.isf(1/10, mu, sigma)
val_tau_100 = norm.isf(1/100, mu, sigma)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig = plt.figure(figsize=(8, 5))
plt.scatter(x, y, s=20, marker='o', edgecolor='#222831',
            facecolor='#00ADB5', alpha=0.6)


tg = tglobal.values
plt.plot(tg, mean, c='#FF2E63', lw=1.5, label='Mean')
plt.plot(tg, mean_plus_1std, c='#FF2E63', lw=0.5)
plt.plot(tg, mean_plus_2std, c='#FF2E63', lw=0.5)
plt.plot(tg, val_tau_100, c='#FF9A00', lw=1.5, label='100-year event')
plt.plot(tg, val_tau_10, c='#FF9A00', lw=1.5, ls='--', label='10-year event')
# plt.ylim([35, 43])
# plt.xlim([-0.2, 1.0])
plt.grid(color='grey', lw=0.4, ls='--')
ax = plt.gca()
ax.tick_params(direction="in")
plt.xlabel('Global mean surface temperature anomaly (smoothed) [ºC]')
plt.ylabel('Tmax [DJF, 30-40ºS] (ºC)')
plt.legend(loc='upper center', ncol=3)
plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/LENS1_tmax_1d_GMST_norm.png',
            dpi=300)
plt.show()
