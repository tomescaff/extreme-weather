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

MLE_lens1_hdi_be = np.zeros((n,))
MLE_lens1_hdi_lo = np.zeros((n,))
MLE_lens1_hdi_hi = np.zeros((n,))

MLE_lens1_fdi_be = np.zeros((n,))
MLE_lens1_fdi_lo = np.zeros((n,))
MLE_lens1_fdi_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.MLE_all_estimate_norm(df, model, Tg_ac=0.90, tau=tau)
    MLE_lens1_hdi_be[i] = df.loc['Best estimate', 'Delta ac-pa']
    MLE_lens1_hdi_lo[i] = df.loc['Lower estimate', 'Delta ac-pa']
    MLE_lens1_hdi_hi[i] = df.loc['Upper estimate', 'Delta ac-pa']

    MLE_lens1_fdi_be[i] = df.loc['Best estimate', 'Delta fu-ac']
    MLE_lens1_fdi_lo[i] = df.loc['Lower estimate', 'Delta fu-ac']
    MLE_lens1_fdi_hi[i] = df.loc['Upper estimate', 'Delta fu-ac']


# obtain LENS1-DE parameters

lens_pa = np.ravel(lens.lens1_tmax_1d_djf_30_40S_cr().values)
lens_ac = np.ravel(lens.lens1_tmax_1d_djf_30_40S_40m_present().values)
lens_fu = np.ravel(lens.lens1_tmax_1d_djf_30_40S_40m_future().values)

nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'DE_LENS1_tmax_1d_30_40S_nboot_{nboot}_norm_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

DE_lens1_hdi_be = np.zeros((n,))
DE_lens1_hdi_lo = np.zeros((n,))
DE_lens1_hdi_hi = np.zeros((n,))

DE_lens1_fdi_be = np.zeros((n,))
DE_lens1_fdi_lo = np.zeros((n,))
DE_lens1_fdi_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.DE_all_estimate_norm(lens_pa, lens_ac, lens_fu, model, tau)
    DE_lens1_hdi_be[i] = df.loc['Best estimate', 'Delta ac-pa']
    DE_lens1_hdi_lo[i] = df.loc['Lower estimate', 'Delta ac-pa']
    DE_lens1_hdi_hi[i] = df.loc['Upper estimate', 'Delta ac-pa']

    DE_lens1_fdi_be[i] = df.loc['Best estimate', 'Delta fu-ac']
    DE_lens1_fdi_lo[i] = df.loc['Lower estimate', 'Delta fu-ac']
    DE_lens1_fdi_hi[i] = df.loc['Upper estimate', 'Delta fu-ac']

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
ax.fill_between(x, MLE_lens1_hdi_lo, MLE_lens1_hdi_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, MLE_lens1_hdi_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, MLE_lens1_fdi_lo, MLE_lens1_fdi_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, MLE_lens1_fdi_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(loc='upper right', ncol=1)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Intensity change (ºC)')
ax.set_xscale('log')
ax.text(11, 1.85, 'a) CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0.5, 2])

ax = axs[0, 1]
ax.fill_between(x, DE_lens1_hdi_lo, DE_lens1_hdi_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, DE_lens1_hdi_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, DE_lens1_fdi_lo, DE_lens1_fdi_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, DE_lens1_fdi_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(loc='upper right', ncol=1)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Intensity change (ºC)')
ax.set_xscale('log')
ax.text(11, 1.85, 'a) CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0.5, 2])

ax = axs[1, 0]
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Intensity change (ºC)')
ax.set_xscale('log')
ax.text(11, 1.85, 'c) CESM2-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0.5, 2])

ax = axs[2, 0]
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Intensity change (ºC)')
ax.set_xscale('log')
ax.text(11, 1.85, 'e) EC Earth 3')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0.5, 2])

ax = axs[3, 0]
x = np.linspace(xmin, xmax, 100)
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Intensity change (ºC)')
ax.set_xscale('log')
ax.text(11, 1.85, 'g) Model Z')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0.5, 2])

axs[0, 0].set_title('Method #1')
axs[0, 1].set_title('Method #2')

plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/summary_deltai_norm.png',
            dpi=300)
