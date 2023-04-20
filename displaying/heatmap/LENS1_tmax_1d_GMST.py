import sys
import cmaps
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev

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

heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]


n, m = heatmap.shape
heatmap_norm = np.zeros((n, m))

for i in range(n):
    for j in range(m):
        heatmap_norm[i, j] = heatmap[i, j]/np.sum(heatmap[i, :])

aspect = (5 - -0.5)/(48-31)
init_params = [37, 4, 2, 0.0]

xopt = (36.84415458460971,
        1.317664562583484,
        1.1486856501249845,
        0.18845359721240793)

# mu0, sigma, alpha, eta = pmath.mle_gev_2d(y, x, init_params)
mu0, sigma, alpha, eta = xopt

mu = mu0 + alpha*x
mu_plus_1sigma = mu + sigma
mu_plus_2sigma = mu + 2*sigma
val_tau_10 = gev.isf(1/10, eta, mu, sigma)
val_tau_100 = gev.isf(1/100, eta, mu, sigma)

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
plt.imshow(heatmap_norm.T, extent=extent, origin='lower',
           cmap=cmaps.MPL_Blues, vmin=0, vmax=0.12, interpolation='gaussian')

plt.plot(x, mu, c='#FF2E63', lw=1.5, label='Mean')
plt.plot(x, mu_plus_1sigma, c='#FF2E63', lw=0.5)
plt.plot(x, mu_plus_2sigma, c='#FF2E63', lw=0.5)
plt.plot(x, val_tau_100, c='#FF9A00', lw=1.5, label='100-year event')
plt.plot(x, val_tau_10, c='#FF9A00', lw=1.5, ls='--', label='10-year event')
ax = plt.gca()
ax.set_aspect('auto')
ax.tick_params(direction="in")
plt.xlabel('Global mean surface temperature anomaly (smoothed) [ºC]')
plt.ylabel('Tmax [DJF, 30-40ºS] (ºC)')
plt.legend(loc='upper center', ncol=3)
plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/LENS1_tmax_1d_GMST_heatmap.png',
            dpi=300)
plt.show()
