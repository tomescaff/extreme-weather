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

# obtain CR2MET-MLE parameters
basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_norm_' +\
    'no2017_no2023_evaluation.csv'
filepath = basedir + filename
df = pd.read_csv(filepath, index_col=0)

nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_CR2MET_tmax_1d_30_40S_nboot_{nboot}_norm_' +\
    'no2017_no2023_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

MLE_cr2met_hpr_be = np.zeros((n,))
MLE_cr2met_hpr_lo = np.zeros((n,))
MLE_cr2met_hpr_hi = np.zeros((n,))

MLE_cr2met_fpr_be = np.zeros((n,))
MLE_cr2met_fpr_lo = np.zeros((n,))
MLE_cr2met_fpr_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.MLE_all_estimate_norm(df, model, Tg_ac=0.90, tau=tau)
    MLE_cr2met_hpr_be[i] = df.loc['Best estimate', 'PR ac-pa']
    MLE_cr2met_hpr_lo[i] = df.loc['Lower estimate', 'PR ac-pa']
    MLE_cr2met_hpr_hi[i] = df.loc['Upper estimate', 'PR ac-pa']

    MLE_cr2met_fpr_be[i] = df.loc['Best estimate', 'PR fu-ac']
    MLE_cr2met_fpr_lo[i] = df.loc['Lower estimate', 'PR fu-ac']
    MLE_cr2met_fpr_hi[i] = df.loc['Upper estimate', 'PR fu-ac']


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

MLE_lens1_hpr_be = np.zeros((n,))
MLE_lens1_hpr_lo = np.zeros((n,))
MLE_lens1_hpr_hi = np.zeros((n,))

MLE_lens1_fpr_be = np.zeros((n,))
MLE_lens1_fpr_lo = np.zeros((n,))
MLE_lens1_fpr_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.MLE_all_estimate_norm(df, model, Tg_ac=0.90, tau=tau)
    MLE_lens1_hpr_be[i] = df.loc['Best estimate', 'PR ac-pa']
    MLE_lens1_hpr_lo[i] = df.loc['Lower estimate', 'PR ac-pa']
    MLE_lens1_hpr_hi[i] = df.loc['Upper estimate', 'PR ac-pa']

    MLE_lens1_fpr_be[i] = df.loc['Best estimate', 'PR fu-ac']
    MLE_lens1_fpr_lo[i] = df.loc['Lower estimate', 'PR fu-ac']
    MLE_lens1_fpr_hi[i] = df.loc['Upper estimate', 'PR fu-ac']


# obtain LENS2-MLE parameters
basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_LENS2_tmax_1d_30_40S_best_estimate_norm_evaluation.csv'
filepath = basedir + filename
df = pd.read_csv(filepath, index_col=0)

nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_LENS2_tmax_1d_30_40S_nboot_{nboot}_norm_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

MLE_lens2_hpr_be = np.zeros((n,))
MLE_lens2_hpr_lo = np.zeros((n,))
MLE_lens2_hpr_hi = np.zeros((n,))

MLE_lens2_fpr_be = np.zeros((n,))
MLE_lens2_fpr_lo = np.zeros((n,))
MLE_lens2_fpr_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.MLE_all_estimate_norm(df, model, Tg_ac=1.10, tau=tau)
    MLE_lens2_hpr_be[i] = df.loc['Best estimate', 'PR ac-pa']
    MLE_lens2_hpr_lo[i] = df.loc['Lower estimate', 'PR ac-pa']
    MLE_lens2_hpr_hi[i] = df.loc['Upper estimate', 'PR ac-pa']

    MLE_lens2_fpr_be[i] = df.loc['Best estimate', 'PR fu-ac']
    MLE_lens2_fpr_lo[i] = df.loc['Lower estimate', 'PR fu-ac']
    MLE_lens2_fpr_hi[i] = df.loc['Upper estimate', 'PR fu-ac']

# obtain ACCESS-MLE parameters
basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_ACCESS_tmax_1d_30_40S_best_estimate_norm_evaluation.csv'
filepath = basedir + filename
df = pd.read_csv(filepath, index_col=0)

nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_ACCESS_tmax_1d_30_40S_nboot_{nboot}_norm_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

MLE_access_hpr_be = np.zeros((n,))
MLE_access_hpr_lo = np.zeros((n,))
MLE_access_hpr_hi = np.zeros((n,))

MLE_access_fpr_be = np.zeros((n,))
MLE_access_fpr_lo = np.zeros((n,))
MLE_access_fpr_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.MLE_all_estimate_norm(df, model, Tg_ac=1.10, tau=tau)
    MLE_access_hpr_be[i] = df.loc['Best estimate', 'PR ac-pa']
    MLE_access_hpr_lo[i] = df.loc['Lower estimate', 'PR ac-pa']
    MLE_access_hpr_hi[i] = df.loc['Upper estimate', 'PR ac-pa']

    MLE_access_fpr_be[i] = df.loc['Best estimate', 'PR fu-ac']
    MLE_access_fpr_lo[i] = df.loc['Lower estimate', 'PR fu-ac']
    MLE_access_fpr_hi[i] = df.loc['Upper estimate', 'PR fu-ac']


# obtain ECEarth3-MLE parameters
basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_ECEarth3_tmax_1d_30_40S_best_estimate_norm_evaluation.csv'
filepath = basedir + filename
df = pd.read_csv(filepath, index_col=0)

nboot = 10
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_ECEarth3_tmax_1d_30_40S_nboot_{nboot}_norm_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

MLE_ecearth3_hpr_be = np.zeros((n,))
MLE_ecearth3_hpr_lo = np.zeros((n,))
MLE_ecearth3_hpr_hi = np.zeros((n,))

MLE_ecearth3_fpr_be = np.zeros((n,))
MLE_ecearth3_fpr_lo = np.zeros((n,))
MLE_ecearth3_fpr_hi = np.zeros((n,))

for i, tau in enumerate(x):
    df = metrics.MLE_all_estimate_norm(df, model, Tg_ac=1.10, tau=tau)
    MLE_ecearth3_hpr_be[i] = df.loc['Best estimate', 'PR ac-pa']
    MLE_ecearth3_hpr_lo[i] = df.loc['Lower estimate', 'PR ac-pa']
    MLE_ecearth3_hpr_hi[i] = df.loc['Upper estimate', 'PR ac-pa']

    MLE_ecearth3_fpr_be[i] = df.loc['Best estimate', 'PR fu-ac']
    MLE_ecearth3_fpr_lo[i] = df.loc['Lower estimate', 'PR fu-ac']
    MLE_ecearth3_fpr_hi[i] = df.loc['Upper estimate', 'PR fu-ac']

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

# cr2met
ax = axs[0, 0]
ax.fill_between(x, MLE_cr2met_hpr_lo, MLE_cr2met_hpr_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, MLE_cr2met_hpr_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, MLE_cr2met_fpr_lo, MLE_cr2met_fpr_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, MLE_cr2met_fpr_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(loc='lower right', ncol=1)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.set_yscale('log')
ax.text(11, 7000, 'CR2MET')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 10000])

# cesm1-lens
ax = axs[1, 0]
ax.fill_between(x, MLE_lens1_hpr_lo, MLE_lens1_hpr_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, MLE_lens1_hpr_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, MLE_lens1_fpr_lo, MLE_lens1_fpr_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, MLE_lens1_fpr_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
# ax.legend(loc='center left', ncol=1)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

# cesm2-lens
ax = axs[2, 0]
ax.fill_between(x, MLE_lens2_hpr_lo, MLE_lens2_hpr_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, MLE_lens2_hpr_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, MLE_lens2_fpr_lo, MLE_lens2_fpr_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, MLE_lens2_fpr_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'CESM2-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

# access
ax = axs[3, 0]
ax.fill_between(x, MLE_access_hpr_lo, MLE_access_hpr_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, MLE_access_hpr_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, MLE_access_fpr_lo, MLE_access_fpr_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, MLE_access_fpr_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'ACCESS-ESM1-5')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

# ecearth3
ax = axs[0, 1]
ax.fill_between(x, MLE_ecearth3_hpr_lo, MLE_ecearth3_hpr_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, MLE_ecearth3_hpr_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, MLE_ecearth3_fpr_lo, MLE_ecearth3_fpr_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, MLE_ecearth3_fpr_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'EC-Earth 3')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

ax = axs[1, 1]
x = np.linspace(xmin, xmax, 100)
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'Model Y')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

ax = axs[2, 1]
x = np.linspace(xmin, xmax, 100)
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(11, 27.5, 'Model Z')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/summary_PR_norm_MLE.png',
            dpi=300)
