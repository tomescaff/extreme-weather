import sys
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum
from scipy.stats import genextreme as dist
from scipy.stats import kstest
from sklearn.utils import resample as bootstrap

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402
from utilities import cr2met  # noqa: E402
from utilities import math as pmath  # noqa: E402

tlocal = cr2met.tmax_1d_djf_30_40S()
t2017 = tlocal.sel(time='2017').values
t2023 = tlocal.sel(time='2023').values
x, y = metrics.obs_data_tmax_1d_remove_year(tlocal_year_to_remove=[2017, 2023])
data = np.ravel(y)

basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_gev' +\
    '_no2017_no2023_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0 = df.loc['Best estimate', 'mu0']
sigma = df.loc['Best estimate', 'sigma']
alpha = df.loc['Best estimate', 'alpha']
eta = df.loc['Best estimate', 'eta']

mu = mu0 + alpha*x
mu_act = mu0 + alpha*1.1
y_mean = dist.mean(eta, mu, sigma)
mean_act = dist.mean(eta, mu_act, sigma)
y_act = y - y_mean + mean_act

ymin, ymax = 30, 50
y_rp = np.linspace(ymin, ymax, 1000)
x_rp = 1/dist.sf(y_rp, eta, mu_act, sigma)
y_rp_dist = dist.isf(1/x_rp, eta, mu_act, sigma)
# compute non parametric tau
u, tau = pmath.return_periods(y_act, method='up')


# CI of the mean
nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_CR2MET_tmax_1d_30_40S_nboot_{nboot}' +\
    '_gev_no2017_no2023_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)
boot_mu0 = model.mu0.values
boot_alpha = model.alpha.values
boot_sigma = model.sigma.values
boot_eta = model.eta.values

boot_mu = boot_mu0 + 1.1*boot_alpha
bspreds = np.zeros((nboot, y_rp_dist.size))

for i in range(nboot):
    bspreds[i, :] = 1/dist.sf(y_rp_dist, boot_eta[i],
                              boot_mu[i], boot_sigma[i])

xinf, xsup = np.quantile(bspreds, [0.025, 0.975], axis=0)

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

plt.scatter(tau, u, marker='o', facecolor='#65647C',
            edgecolor='#000000', alpha=0.7, label='CR2MET')

plt.plot(x_rp, y_rp_dist, color='#FC2947', lw=1.5, label='fit')
plt.plot(xinf[xinf > 10], y_rp_dist[xinf > 10], color='#FC2947', lw=0.5)
plt.plot(xsup[xsup > 10], y_rp_dist[xsup > 10], color='#FC2947', lw=0.5)

# set grid
plt.grid(lw=0.2, ls='--', color='grey')

# set x log scale
plt.gca().set_xscale('log')

# set ticks and lims
xticks = np.arange(1, 11, 1)
xticks = np.append(xticks, [xticks*z for z in [1e2, 1e3, 1e4]])
plt.axhline(t2017, c='r', lw=1.0, label='2017')
plt.axhline(t2023, c='b', lw=1.0, label='2023')
plt.xticks(xticks)
plt.xlim([0.9, 1000])
plt.ylim([ymin, ymax])

# set title and labels
plt.xlabel('Return period (yr)')
plt.ylabel('Tmax (ºC)')

# set legend
plt.legend()


# set title and labels
basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_return_period_MLE_gev.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
