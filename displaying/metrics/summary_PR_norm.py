import sys
import numpy as np
import pandas as pd
import xarray as xr
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

xmin, xmax = 1e1, 1e4
n = 100
x = np.logspace(1, 4, n, base=10)

# obtain LENS1-MLE parameters

basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_LENS1_tmax_1d_30_40S_best_estimate_norm_evaluation.csv'
filepath = basedir + filename
df = pd.read_csv(filepath, index_col=0)

nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_LENS1_tmax_1d_30_40S_nboot_{nboot}_norm_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

lens1_hpr_be = np.zeros((n,))
lens1_hpr_lo = np.zeros((n,))
lens1_hpr_hi = np.zeros((n,))

lens1_fpr_be = np.zeros((n,))
lens1_fpr_lo = np.zeros((n,))
lens1_fpr_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.MLE_all_estimate_norm(df, model, Tg_ac=0.90, tau=tau)
    lens1_hpr_be[i] = df.loc['Best estimate', 'PR ac-pa']
    lens1_hpr_lo[i] = df.loc['Lower estimate', 'PR ac-pa']
    lens1_hpr_hi[i] = df.loc['Upper estimate', 'PR ac-pa']

    lens1_fpr_be[i] = df.loc['Best estimate', 'PR fu-ac']
    lens1_fpr_lo[i] = df.loc['Lower estimate', 'PR fu-ac']
    lens1_fpr_hi[i] = df.loc['Upper estimate', 'PR fu-ac']

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False


fig, axs = plt.subplots(4, 2, figsize=(10, 10))

ax = axs[0, 0]
ax.fill_between(x, lens1_hpr_lo, lens1_hpr_hi, color='#0B2447', alpha=0.2)
ax.plot(x, lens1_hpr_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, lens1_fpr_lo, lens1_fpr_hi, color='#FC2947', alpha=0.2)
ax.plot(x, lens1_fpr_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(loc='center left', ncol=1)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'a) CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

ax = axs[1, 0]
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'c) CESM2-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

ax = axs[2, 0]
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'e) EC Earth 3')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

ax = axs[3, 0]
x = np.linspace(xmin, xmax, 100)
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'g) Model Z')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

axs[0, 0].set_title('Method #1')
axs[0, 1].set_title('Method #2')

plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/summary_PR_norm.png',
            dpi=300)
