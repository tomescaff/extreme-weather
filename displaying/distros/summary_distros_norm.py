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

# obtain LENS1-MLE parameters

# method 1
basedir = '/home/tcarrasco/result/data/all_estimate/'
filename = 'MLE_LENS1_tmax_1d_30_40S_all_estimate_' +\
    'nboot_1000_tau_100_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0, sigma, alpha, ev_ac = df.loc['Best estimate',
                                  ['mu0', 'sigma', 'alpha', 'ev_ac']]
MLE_lens1_mu_pa = mu0
MLE_lens1_mu_ac = mu0 + alpha*0.9  # 0.9 ºC is the LENS1 2011-2020 GMST
MLE_lens1_mu_fu = mu0 + alpha*2.0  # 2.0 ºC warmer world is future
MLE_lens1_sigma = sigma
MLE_lens1_ev_ac = ev_ac

# method 2
basedir = '/home/tcarrasco/result/data/all_estimate/'
filename = 'DE_LENS1_tmax_1d_30_40S_all_estimate_' +\
    'nboot_1000_tau_100_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)

mu_pa, mu_ac, mu_fu = df.loc['Best estimate', ['mu_pa', 'mu_ac', 'mu_fu']]
sd_pa, sd_ac, sd_fu = df.loc['Best estimate', ['sig_pa', 'sig_ac', 'sig_fu']]

DE_lens1_mu_pa = mu_pa
DE_lens1_mu_ac = mu_ac
DE_lens1_mu_fu = mu_fu
DE_lens1_sig_pa = sd_pa
DE_lens1_sig_ac = sd_ac
DE_lens1_sig_fu = sd_fu
DE_lens1_ev_ac = df.loc['Best estimate', 'ev_ac']

# obtain LENS2-MLE parameters

# method 1
basedir = '/home/tcarrasco/result/data/all_estimate/'
filename = 'MLE_LENS2_tmax_1d_30_40S_all_estimate_' +\
    'nboot_1000_tau_100_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0, sigma, alpha, ev_ac = df.loc['Best estimate',
                                  ['mu0', 'sigma', 'alpha', 'ev_ac']]
MLE_lens2_mu_pa = mu0
MLE_lens2_mu_ac = mu0 + alpha*1.1  # 1.1 ºC is the LENS2 2011-2020 GMST
MLE_lens2_mu_fu = mu0 + alpha*2.0  # 2.0 ºC warmer world is future
MLE_lens2_sigma = sigma
MLE_lens2_ev_ac = ev_ac


# plot

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

xmin, xmax = 30, 50
x = np.linspace(xmin, xmax, 100)

fig, axs = plt.subplots(4, 2, figsize=(10, 10))

ax = axs[0, 0]
ax.plot(x, norm.pdf(x, MLE_lens1_mu_ac, MLE_lens1_sigma),
        c='#159895', lw=2)
ax.fill_between(x, 0, norm.pdf(x, MLE_lens1_mu_ac, MLE_lens1_sigma),
                color='#159895', alpha=0.5, label='Factual')
ax.plot(x, norm.pdf(x, MLE_lens1_mu_pa, MLE_lens1_sigma),
        c='#0B2447', lw=1, ls='--', label='Counterfactual')
ax.plot(x, norm.pdf(x, MLE_lens1_mu_fu, MLE_lens1_sigma),
        c='#FC2947', lw=1, ls='--', label='Future')
ax.axvline(MLE_lens1_ev_ac,
           c='fuchsia', lw=1, label='100-year event\n(factual climate)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(ncol=1)
ax.set_xlabel('Highest Tx [DJF, central Chile] (ºC)')
ax.set_ylabel('PDF')
ax.text(30.5, 0.45, 'a) CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

ax = axs[0, 1]
ax.plot(x, norm.pdf(x, DE_lens1_mu_ac, DE_lens1_sig_ac),
        c='#159895', lw=2)
ax.fill_between(x, 0, norm.pdf(x, DE_lens1_mu_ac, DE_lens1_sig_ac),
                color='#159895', alpha=0.5, label='Factual')
ax.plot(x, norm.pdf(x, DE_lens1_mu_pa, DE_lens1_sig_pa),
        c='#0B2447', lw=1, ls='--', label='Counterfactual')
ax.plot(x, norm.pdf(x, DE_lens1_mu_fu, DE_lens1_sig_fu),
        c='#FC2947', lw=1, ls='--', label='Future')
ax.axvline(MLE_lens1_ev_ac,
           c='fuchsia', lw=1, label='100-year event\n(factual climate)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
# ax.legend(ncol=1)
ax.set_xlabel('Highest Tx [DJF, central Chile] (ºC)')
ax.set_ylabel('PDF')
ax.text(30.5, 0.45, 'a) CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

ax = axs[1, 0]
ax.plot(x, norm.pdf(x, MLE_lens2_mu_ac, MLE_lens2_sigma),
        c='#159895', lw=2)
ax.fill_between(x, 0, norm.pdf(x, MLE_lens2_mu_ac, MLE_lens2_sigma),
                color='#159895', alpha=0.5, label='Factual')
ax.plot(x, norm.pdf(x, MLE_lens2_mu_pa, MLE_lens2_sigma),
        c='#0B2447', lw=1, ls='--', label='Counterfactual')
ax.plot(x, norm.pdf(x, MLE_lens2_mu_fu, MLE_lens2_sigma),
        c='#FC2947', lw=1, ls='--', label='Future')
ax.axvline(MLE_lens2_ev_ac,
           c='fuchsia', lw=1, label='100-year event\n(factual climate)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Highest Tx [DJF, central Chile] (ºC)')
ax.set_ylabel('PDF')
ax.text(30.5, 0.45, 'c) CESM2-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

ax = axs[2, 0]
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Highest Tx [DJF, central Chile] (ºC)')
ax.set_ylabel('PDF')
ax.text(30.5, 0.45, 'e) EC Earth 3')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

ax = axs[3, 0]
x = np.linspace(xmin, xmax, 100)
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Highest Tx [DJF, central Chile] (ºC)')
ax.set_ylabel('PDF')
ax.text(30.5, 0.45, 'g) Model Z')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

axs[0, 0].set_title('Method #1')
axs[0, 1].set_title('Method #2')

plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/summary_distros_norm.png',
            dpi=300)
