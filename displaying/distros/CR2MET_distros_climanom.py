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


x, y = metrics.obs_data_tmax_1d()
init_params = [35, 2, 2, 0.1]
mu0, sigma, alpha, eta = pmath.mle_gev_2d(y, x, init_params)
mu = mu0 + alpha*x
data = y - gev.mean(eta, mu, sigma)

fit_nor = norm.fit(data)
fit_gev = gev.fit(data)
fit_gum = gum.fit(data)

# test fit
stat, p_norm = kstest(data, 'norm', fit_nor)
stat, p_gev = kstest(data, 'genextreme', fit_gev)
stat, p_gum = kstest(data, 'gumbel_r', fit_gum)

# compute histogram
hist, bins = np.histogram(data, bins=np.linspace(-10, 20, 20), density=True)

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
fig = plt.figure(figsize=(8, 6))

# plot the histogram
width = 0.85 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width, edgecolor='#000000',
        facecolor='#65647C', alpha=0.7, lw=0.2, label='CR2MET Tmax anom (GEV)')
plt.xlim([-10, 20])

# plot the PDFs
x = np.linspace(-10, 20, 100)
plt.plot(x, norm.pdf(x, *fit_nor), c='#0B2447', linewidth=2,
         label='Norm fit (p = {:g})'.format(p_norm))
plt.plot(x, gev.pdf(x, *fit_gev), c='#159895', linewidth=2,
         label='GEV fit (p = {:g})'.format(p_gev))
plt.plot(x, gum.pdf(x, *fit_gum), c='#FC2947', linewidth=2,
         label='Gumbel fit (p = {:g})'.format(p_gum))

# set grid
plt.grid(lw=0.2, ls='--', color='grey')

# set legend
plt.legend()

plt.xlabel('Tmax (ºC)')
plt.ylabel('PDF')

# set title and labels
basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_climanom_distros.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
