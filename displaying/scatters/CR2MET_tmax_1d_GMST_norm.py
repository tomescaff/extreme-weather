import sys
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import norm

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import cr2met  # noqa: E402
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402

tglobal = gmst.annual_5year_smooth()
tlocal = cr2met.tmax_1d_djf_30_40S()

x_prev = tglobal.sel(time=slice('1959', '1978'))
y_prev = tlocal.sel(time=slice('1960', '1979'))

x = tglobal.sel(time=slice('1979', '2022'))
y = tlocal.sel(time=slice('1980', '2023'))

basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0 = df.loc['Best estimate', 'mu0']
sigma = df.loc['Best estimate', 'sigma']
alpha = df.loc['Best estimate', 'alpha']

mu = mu0 + alpha*x
mean = norm.mean(mu, sigma)
std = norm.std(mu, sigma)
mean_plus_1std = mean + std
mean_plus_2std = mean + 2*std
val_tau_10 = norm.isf(1/10, mu, sigma)
val_tau_100 = norm.isf(1/100, mu, sigma)
val_tau_1000 = norm.isf(1/1000, mu, sigma)

# CI of the mean
nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_CR2MET_tmax_1d_30_40S_nboot_{nboot}_norm_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)
boot_mu0 = model.mu0.values
boot_alpha = model.alpha.values
boot_sigma = model.sigma.values

xx = np.linspace(x.min('time').values, x.max('time').values, 100)
mean_mat = np.zeros((nboot, xx.size))

for i, x_ in enumerate(xx):

    mu_arr = boot_mu0 + boot_alpha*x_

    for j, mu_ in enumerate(mu_arr):
        mean_mat[j, i] = norm.mean(mu_, boot_sigma[j])

mean_inf, mean_sup = np.quantile(mean_mat, [0.025, 0.975], axis=0)


# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
# plt.rcParams['axes.spines.top'] = False
# plt.rcParams['axes.spines.right'] = False

fig = plt.figure(figsize=(8, 5))
plt.fill_between(xx, mean_inf, mean_sup, color='#FFDEDE')
# plt.scatter(x_prev, y_prev, s=20, marker='o',
#             edgecolor='#222831', facecolor='#EEEEEE', alpha=0.8)
plt.scatter(x, y, s=20, marker='o', edgecolor='#222831',
            facecolor='#00ADB5', alpha=0.8)

for year in [2017, 2023]:
    plt.text(x.sel(time=f'{year-1}')+0.01,
             y.sel(time=f'{year}'), f'{year}', fontsize=7)

plt.text(x.sel(time=f'{2019-1}')-0.03,
         y.sel(time=f'{2019}')-0.1, f'{2019}', fontsize=7)

plt.plot(x, mean, c='#FF2E63', lw=2.0, label='Mean')
plt.plot(x, mean_plus_1std, c='#FF2E63', lw=0.5, label='Mean + Std')
# plt.plot(x, mean_plus_2std, c='#FF2E63', lw=0.5)
plt.plot(x, val_tau_10, c='#FF9A00', lw=1.5, ls='-.', label='10-year event')
plt.plot(x, val_tau_100, c='#FF9A00', lw=1.5, ls='--', label='100-year event')
plt.plot(x, val_tau_1000, c='#FF9A00', lw=1.5, ls='dotted',
         label='1000-year event')
plt.ylim([35, 43])
plt.xlim([x.min()-0.01, x.max()+0.01])
plt.grid(color='grey', lw=0.4, ls='--')
ax = plt.gca()
# ax.tick_params(direction="in")
plt.xlabel('GMST anomaly (smoothed) (ºC)')
plt.ylabel('Highest Tx (ºC)')
plt.legend(loc='lower right', ncol=2, facecolor='white', framealpha=1)
plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/CR2MET_tmax_1d_GMST_mean.png',
            dpi=300)
plt.show()
