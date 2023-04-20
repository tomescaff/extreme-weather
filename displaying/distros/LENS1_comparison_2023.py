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
tl = lens.lens1_tmax_1d_djf_30_40S_40m()
tg = gmst.annual_lens1_ensmean()
# gev
# init_params = [36.8, 1.3, 1.1, 0.1]
# mu0, sigma, alpha, eta = pmath.mle_gev_2d(y, x, init_params)
# print(mu0, sigma, alpha, eta)
mu0 = 36.84408841810675
sigma = 1.3176836243310976
alpha = 1.1486964600845266
eta = 0.18841727839206607

mu = mu0 + alpha*tg
mu_2023 = mu.sel(time='2023').values

data_10yr = np.ravel(tl.sel(time=slice('2018', '2028')).values)
data_30yr = np.ravel(tl.sel(time=slice('2008', '2038')).values)

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
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

xmin, xmax = 30, 50
x = np.linspace(xmin, xmax, 100)
plt.sca(axs[0])
plt.plot(x, gev.pdf(x, eta, mu_2023, sigma), c='#159895',
         linewidth=2, label='Tglobal fit', ls='--')
plt.plot(x, gev.pdf(x, *gev.fit(data_10yr)), c='#FC2947',
         linewidth=2, label='10yr fit', ls='--')
plt.plot(x, gev.pdf(x, *gev.fit(data_30yr)), c='#0B2447',
         linewidth=2, label='30yr fit', ls='--')
plt.grid(lw=0.2, ls='--', color='grey')
plt.legend()
plt.xlim([xmin, xmax])
plt.xlabel('Tmax (ºC)')
plt.ylabel('PDF')

plt.sca(axs[1])
y = np.linspace(xmin, xmax, 1000)
x = 1/gev.sf(y, eta, mu_2023, sigma)
y_tglob = gev.isf(1/x, eta, mu_2023, sigma)
y_10yr = gev.isf(1/x, *gev.fit(data_10yr))
y_30yr = gev.isf(1/x, *gev.fit(data_30yr))
plt.plot(x, y_30yr, color='#0B2447', lw=1.5, alpha=1, label='Normal')
plt.plot(x, y_tglob, color='#159895', lw=1.5, alpha=1, label='GEV')
plt.plot(x, y_10yr, color='#FC2947', lw=1.5, alpha=1, label='Gumbel')
plt.grid(lw=0.2, ls='--', color='grey')
plt.gca().set_xscale('log')
xticks = np.arange(1, 11, 1)
xticks = np.append(xticks, [xticks*z for z in [1e2, 1e3, 1e4]])
plt.xticks(xticks)
plt.xlim([0.9, 60000])
plt.ylim([xmin, xmax])
plt.xlabel('Return period (yr)')
plt.ylabel('Tmax (ºC)')
plt.legend()

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_comparison_2023.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
