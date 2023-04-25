import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum
from scipy.stats import norm
from scipy.stats import kstest

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import lens  # noqa: E402
from utilities import metrics  # noqa: E402
from utilities import math as pmath  # noqa: E402


tg, tl = metrics.lens1_data_tmax_1d()

basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_gev_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0_lens1 = df.loc['Best estimate', 'mu0']
sigma_lens1 = df.loc['Best estimate', 'sigma']
alpha_lens1 = df.loc['Best estimate', 'alpha']
eta_lens1 = df.loc['Best estimate', 'eta']

mu_pa_lens1 = mu0_lens1
mu_ac_lens1 = mu0_lens1 + alpha_lens1*0.9  # 0.9 ºC is the LENS1 2011-2020 GMST
mu_fu_lens1 = mu0_lens1 + alpha_lens1*2.0  # 2.0 ºC warmer world is future

ev_ac_lens1 = gev.isf(1/100, eta_lens1, mu_ac_lens1, sigma_lens1)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
xmin, xmax = 30, 50

ax = axs[0, 0]
x = np.linspace(xmin, xmax, 100)

ax.plot(x, gev.pdf(x, eta_lens1, mu_ac_lens1,
        sigma_lens1), c='#159895', linewidth=2)
ax.fill_between(x, 0, gev.pdf(x, eta_lens1, mu_ac_lens1,
                sigma_lens1), color='#159895', alpha=0.5, label='Factual')
ax.plot(x, gev.pdf(x, eta_lens1, mu_pa_lens1, sigma_lens1),
        c='#0B2447', linewidth=1, ls='--', label='Counterfactual')
ax.plot(x, gev.pdf(x, eta_lens1, mu_fu_lens1, sigma_lens1),
        c='#FC2947', linewidth=1, ls='--', label='Future')
ax.axvline(ev_ac_lens1, c='fuchsia', linewidth=1,
           label='100-year event (Factual)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(ncol=1)
ax.set_xlabel('Tmax (ºC)')
ax.set_ylabel('PDF')
ax.set_title('CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

ax = axs[0, 1]
x = np.linspace(xmin, xmax, 100)

ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Tmax (ºC)')
ax.set_ylabel('PDF')
ax.set_title('CESM2-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

ax = axs[1, 0]
x = np.linspace(xmin, xmax, 100)

ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
# ax.legend(ncol=1)
ax.set_xlabel('Tmax (ºC)')
ax.set_ylabel('PDF')
ax.set_title('EC Earth3')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

ax = axs[1, 1]
x = np.linspace(xmin, xmax, 100)
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
# ax.legend(ncol=1)
ax.set_xlabel('Tmax (ºC)')
ax.set_ylabel('PDF')
ax.set_title('Model Z')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])


plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/MLE_summary_distros.png',
            dpi=300)
# plt.show()
