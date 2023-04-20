import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402
from utilities import gmst, lens  # noqa: E402
from utilities import math as pmath  # noqa: E402

tg, tl = metrics.lens1_data_tmax_1d()

basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_LENS1_tmax_1d_30_40S_best_estimate_gev_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0_lens1 = df.loc['Best estimate', 'mu0']
sigma_lens1 = df.loc['Best estimate', 'sigma']
alpha_lens1 = df.loc['Best estimate', 'alpha']
eta_lens1 = df.loc['Best estimate', 'eta']

mu_pa_lens1 = mu0_lens1
mu_ac_lens1 = mu0_lens1 + alpha_lens1*0.9  # 0.9 ºC is the LENS1 2011-2020 GMST
mu_fu_lens1 = mu0_lens1 + alpha_lens1*2.0  # 2.0 ºC warmer world is future

ev_ac_lens1 = gev.isf(1/100, eta_lens1, mu_ac_lens1, sigma_lens1)

x_tot = np.linspace(np.min(tg), np.max(tg), 1000)
mu_lens1 = mu0_lens1 + alpha_lens1*x_tot
mean = gev.mean(eta_lens1, mu_lens1, sigma_lens1)
std = gev.std(eta_lens1, mu_lens1, sigma_lens1)
mean_plus_1std = mean + std
mean_plus_2std = mean + 2*std
val_tau_10 = gev.isf(1/10, eta_lens1, mu_lens1, sigma_lens1)
val_tau_100 = gev.isf(1/100, eta_lens1, mu_lens1, sigma_lens1)

# CI
nboot = 100
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_LENS1_tmax_1d_30_40S_nboot_{nboot}_gev_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)
boot_mu0 = model.mu0.values
boot_sigma = model.sigma.values
boot_alpha = model.alpha.values
boot_eta = model.eta.values

mean_mat = np.zeros((nboot, x_tot.size))

for i, x_ in enumerate(x_tot):

    mu_arr = boot_mu0 + boot_alpha*x_

    for j, mu_ in enumerate(mu_arr):
        mean_mat[j, i] = gev.mean(boot_eta[j], mu_, boot_sigma[j])

mean_inf, mean_sup = np.quantile(mean_mat, [0.025, 0.975], axis=0)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig = plt.figure(figsize=(14, 7))
gs = fig.add_gridspec(1, 4,  width_ratios=(4, 1, 4, 1),
                      left=0.1, right=0.9, bottom=0.1, top=0.9,
                      wspace=0.2, hspace=0.07)

ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[0, 1], sharey=ax0)
ymin, ymax = 30, 50

plt.sca(ax0)
plt.scatter(tg, tl, s=20, marker='o', ec='#222831', fc='#00ADB5', alpha=0.8)
plt.fill_between(x_tot, mean_inf, mean_sup, color='#FF2E63', alpha=0.5)
plt.plot(x_tot, mean, c='#FF2E63', lw=1.0, label='Mean')
plt.plot(x_tot, mean_plus_1std, c='#FF2E63', lw=0.5)
plt.plot(x_tot, mean_plus_2std, c='#FF2E63', lw=0.5)
plt.plot(x_tot, val_tau_100, c='#FF9A00', lw=1.5, label='100-year event')
plt.plot(x_tot, val_tau_10, c='#FF9A00',
         lw=1.5, ls='--', label='10-year event')
plt.ylim([ymin, ymax])
# plt.yticks(np.arange(ymin, ymax+1, 2))
plt.xlim([-0.5, 5.5])
plt.grid(color='grey', lw=0.4, ls='--')
ax = plt.gca()
ax.tick_params(direction="in")
ax.set_title('Method #1')
plt.xlabel('GMST anomaly (smoothed) [ºC]')
plt.ylabel('Tmax [DJF, 30-40ºS] (ºC)')
plt.legend(loc='upper center', ncol=3)

plt.sca(ax1)
y = np.linspace(ymin, ymax, 1000)
x = gev.pdf(y, eta_lens1, mu_ac_lens1, sigma_lens1)
plt.fill_betweenx(y, x, color='#00ADB5', alpha=0.5, label='Factual')
plt.plot(x, y, lw=2, c='#00ADB5')
# plt.plot(x, y, lw=0.5, c='k')
x = gev.pdf(y, eta_lens1, mu_pa_lens1, sigma_lens1)
plt.plot(x, y, lw=1, c='#0B2447', ls='--', label='Counterfactual')
x = gev.pdf(y, eta_lens1, mu_fu_lens1, sigma_lens1)
plt.plot(x, y, lw=1, c='#FC2947', ls='--', label='Future')
plt.xlim([0, 0.5])
plt.xlabel('PDF')
ax = plt.gca()
ax.set_axisbelow(True)
ax.tick_params(direction="in")
ax.yaxis.set_tick_params(length=2)
plt.axhline(gev.isf(1/100, eta_lens1, mu_ac_lens1, sigma_lens1),
            c='fuchsia', lw=1, label='100-year event (Factual)')
# plt.axhline(gev.isf(1/100, eta, mu_pa, sigma), c='#FF9A00', lw=0.5)
# plt.axhline(gev.isf(1/100, eta, mu_fu, sigma), c='#FF9A00', lw=0.5)
ax.legend(ncol=1)
basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_methods.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
plt.show()
