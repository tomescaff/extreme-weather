import sys
import numpy as np
import xarray as xr
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
basedir = '/home/tcarrasco/result/data/all_estimate/'
filename = 'MLE_LENS1_tmax_1d_30_40S_all_estimate_' +\
    'nboot_1000_tau_100_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0, sigma, alpha, ev_ac = df.loc['Best estimate',
                                  ['mu0', 'sigma', 'alpha', 'ev_ac']]
MLE_lens1_mu_pa = mu0
MLE_lens1_mu_ac_ = mu0 + alpha*0.9  # 0.9 ºC is the LENS1 2011-2020 GMST
MLE_lens1_mu_fu = mu0 + alpha*2.0  # 2.0 ºC warmer world is future
MLE_lens1_sigma = sigma
MLE_lens1_ev_ac = ev_ac

MLE_lens1_mu_pa = mu0 - MLE_lens1_mu_ac_
MLE_lens1_mu_ac = mu0 + alpha*0.9 - MLE_lens1_mu_ac_
MLE_lens1_mu_fu = mu0 + alpha*2.0 - MLE_lens1_mu_ac_
MLE_lens1_sigma = sigma
MLE_lens1_ev_ac = ev_ac - MLE_lens1_mu_ac_

# obtain LENS2-MLE parameters
basedir = '/home/tcarrasco/result/data/all_estimate/'
filename = 'MLE_LENS2_tmax_1d_30_40S_all_estimate_' +\
    'nboot_1000_tau_100_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0, sigma, alpha, ev_ac = df.loc['Best estimate',
                                  ['mu0', 'sigma', 'alpha', 'ev_ac']]
MLE_lens2_mu_pa = mu0
MLE_lens2_mu_ac_ = mu0 + alpha*1.1  # 1.1 ºC is the LENS2 2011-2020 GMST
MLE_lens2_mu_fu = mu0 + alpha*2.0  # 2.0 ºC warmer world is future
MLE_lens2_sigma = sigma
MLE_lens2_ev_ac = ev_ac

MLE_lens2_mu_pa = mu0 - MLE_lens2_mu_ac_
MLE_lens2_mu_ac = mu0 + alpha*1.1 - MLE_lens2_mu_ac_
MLE_lens2_mu_fu = mu0 + alpha*2.0 - MLE_lens2_mu_ac_
MLE_lens2_sigma = sigma
MLE_lens2_ev_ac = ev_ac - MLE_lens2_mu_ac_

# obtain ACCESS-MLE parameters
basedir = '/home/tcarrasco/result/data/all_estimate/'
filename = 'MLE_ACCESS_tmax_1d_30_40S_all_estimate_' +\
    'nboot_1000_tau_100_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0, sigma, alpha, ev_ac = df.loc['Best estimate',
                                  ['mu0', 'sigma', 'alpha', 'ev_ac']]
MLE_access_mu_pa = mu0
MLE_access_mu_ac_ = mu0 + alpha*1.1  # 1.1 ºC is the ACCESS 2011-2020 GMST
MLE_access_mu_fu = mu0 + alpha*2.0  # 2.0 ºC warmer world is future
MLE_access_sigma = sigma
MLE_access_ev_ac = ev_ac

MLE_access_mu_pa = mu0 - MLE_access_mu_ac_
MLE_access_mu_ac = mu0 + alpha*1.1 - MLE_access_mu_ac_
MLE_access_mu_fu = mu0 + alpha*2.0 - MLE_access_mu_ac_
MLE_access_sigma = sigma
MLE_access_ev_ac = ev_ac - MLE_access_mu_ac_

# obtain ECEarth3-MLE parameters
basedir = '/home/tcarrasco/result/data/all_estimate/'
filename = 'MLE_ECEarth3_tmax_1d_30_40S_all_estimate_' +\
    'nboot_10_tau_100_norm_evaluation.csv'
df = pd.read_csv(basedir + filename, index_col=0)
mu0, sigma, alpha, ev_ac = df.loc['Best estimate',
                                  ['mu0', 'sigma', 'alpha', 'ev_ac']]
MLE_ecearth3_mu_pa = mu0
MLE_ecearth3_mu_ac_ = mu0 + alpha*1.1  # 1.1 ºC is the ACCESS 2011-2020 GMST
MLE_ecearth3_mu_fu = mu0 + alpha*2.0  # 2.0 ºC warmer world is future
MLE_ecearth3_sigma = sigma
MLE_ecearth3_ev_ac = ev_ac

MLE_ecearth3_mu_pa = mu0 - MLE_ecearth3_mu_ac_
MLE_ecearth3_mu_ac = mu0 + alpha*1.1 - MLE_ecearth3_mu_ac_
MLE_ecearth3_mu_fu = mu0 + alpha*2.0 - MLE_ecearth3_mu_ac_
MLE_ecearth3_sigma = sigma
MLE_ecearth3_ev_ac = ev_ac - MLE_ecearth3_mu_ac_

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

xmin, xmax = -10, 10
x = np.linspace(xmin, xmax, 100)

fig, axs = plt.subplots(5, 2, figsize=(10, 10))

# lens1
ax = axs[0, 0]
ax.plot(x, norm.pdf(x, MLE_lens1_mu_ac, MLE_lens1_sigma),
        c='#159895', lw=2)
ax.fill_between(x, 0, norm.pdf(x, MLE_lens1_mu_ac, MLE_lens1_sigma),
                color='#159895', alpha=0.5, label='Actual')
ax.plot(x, norm.pdf(x, MLE_lens1_mu_pa, MLE_lens1_sigma),
        c='#0B2447', lw=1, ls='--', label='Counterfactual')
ax.plot(x, norm.pdf(x, MLE_lens1_mu_fu, MLE_lens1_sigma),
        c='#FC2947', lw=1, ls='--', label='Future')
ax.axvline(MLE_lens1_ev_ac,
           c='fuchsia', lw=1, label='100-year event\n(actual climate)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(ncol=1, loc='upper right', prop={'size': 8})
ax.set_xlabel('Highest Tx anomaly (ºC)')
ax.set_ylabel('PDF')
ax.text(-9.5, 0.45, 'a) CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

# lens2
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
ax.set_xlabel('Highest Tx anomaly (ºC)')
ax.set_ylabel('PDF')
ax.text(-9.5, 0.45, 'c) CESM2-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

# access
ax = axs[2, 0]
ax.plot(x, norm.pdf(x, MLE_access_mu_ac, MLE_access_sigma),
        c='#159895', lw=2)
ax.fill_between(x, 0, norm.pdf(x, MLE_access_mu_ac, MLE_access_sigma),
                color='#159895', alpha=0.5, label='Factual')
ax.plot(x, norm.pdf(x, MLE_access_mu_pa, MLE_access_sigma),
        c='#0B2447', lw=1, ls='--', label='Counterfactual')
ax.plot(x, norm.pdf(x, MLE_access_mu_fu, MLE_access_sigma),
        c='#FC2947', lw=1, ls='--', label='Future')
ax.axvline(MLE_access_ev_ac,
           c='fuchsia', lw=1, label='100-year event\n(factual climate)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Highest Tx anomaly (ºC)')
ax.set_ylabel('PDF')
ax.text(-9.5, 0.45, 'e) ACCESS-ESM1-5')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

# ecearth3
ax = axs[3, 0]
ax.plot(x, norm.pdf(x, MLE_ecearth3_mu_ac, MLE_ecearth3_sigma),
        c='#159895', lw=2)
ax.fill_between(x, 0, norm.pdf(x, MLE_ecearth3_mu_ac, MLE_ecearth3_sigma),
                color='#159895', alpha=0.5, label='Factual')
ax.plot(x, norm.pdf(x, MLE_ecearth3_mu_pa, MLE_ecearth3_sigma),
        c='#0B2447', lw=1, ls='--', label='Counterfactual')
ax.plot(x, norm.pdf(x, MLE_ecearth3_mu_fu, MLE_ecearth3_sigma),
        c='#FC2947', lw=1, ls='--', label='Future')
ax.axvline(MLE_ecearth3_ev_ac,
           c='fuchsia', lw=1, label='100-year event\n(factual climate)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Highest Tx anomaly(ºC)')
ax.set_ylabel('PDF')
ax.text(-9.5, 0.45, 'g) EC-Earth 3')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])


# mirco6
ax = axs[4, 0]
ax.plot(x, norm.pdf(x, MLE_ecearth3_mu_ac, MLE_ecearth3_sigma),
        c='#159895', lw=2)
ax.fill_between(x, 0, norm.pdf(x, MLE_ecearth3_mu_ac, MLE_ecearth3_sigma),
                color='#159895', alpha=0.5, label='Factual')
ax.plot(x, norm.pdf(x, MLE_ecearth3_mu_pa, MLE_ecearth3_sigma),
        c='#0B2447', lw=1, ls='--', label='Counterfactual')
ax.plot(x, norm.pdf(x, MLE_ecearth3_mu_fu, MLE_ecearth3_sigma),
        c='#FC2947', lw=1, ls='--', label='Future')
ax.axvline(MLE_ecearth3_ev_ac,
           c='fuchsia', lw=1, label='100-year event\n(factual climate)')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.set_xlabel('Highest Tx anomaly (ºC)')
ax.set_ylabel('PDF')
ax.text(-9.5, 0.45, 'i) MIROC6')
ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 0.5])

##############################################

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

nboot = 1000
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


# cesm1-lens
ax = axs[0, 1]
ax.fill_between(x, MLE_lens1_hpr_lo, MLE_lens1_hpr_hi,
                color='#0B2447', alpha=0.2)
ax.plot(x, MLE_lens1_hpr_be, c='#0B2447', lw=2, label='Historical')
ax.fill_between(x, MLE_lens1_fpr_lo, MLE_lens1_fpr_hi,
                color='#FC2947', alpha=0.2)
ax.plot(x, MLE_lens1_fpr_be, c='#FC2947', lw=2, label='Future')
ax.grid(lw=0.2, ls='--', color='grey')
ax.set_axisbelow(True)
ax.legend(loc='lower right', ncol=1, prop={'size': 8})
ax.set_xlabel('Return period (yr)')
ax.set_ylabel('Probability ratio')
ax.set_xscale('log')
ax.text(12, 27.5, 'b) CESM1-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

# cesm2-lens
ax = axs[1, 1]
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
ax.text(12, 27.5, 'd) CESM2-LENS')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

# access
ax = axs[2, 1]
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
ax.text(12, 27.5, 'f) ACCESS-ESM1-5')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

# ecearth3
ax = axs[3, 1]
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
ax.text(12, 27.5, 'h) EC-Earth 3')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

# miroc6
ax = axs[4, 1]
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
ax.text(12, 27.5, 'j) MIROC6')
ax.set_xlim([xmin, xmax])
ax.set_ylim([1, 30])

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
plt.savefig(basedir + 'summary_distros_PR_norm_MLE.png',
            dpi=300)
