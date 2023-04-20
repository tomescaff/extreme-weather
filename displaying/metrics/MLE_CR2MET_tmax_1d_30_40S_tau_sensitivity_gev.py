import sys
import numpy as np
import xarray as xr
import pandas as pd
from scipy.stats import genextreme as gev
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from os.path import join

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import gmst  # noqa: E402
from utilities import cr2met  # noqa: E402
from utilities import metrics  # noqa: E402

tglobal_2022 = gmst.annual_5year_smooth().sel(time='2022').values
tlocal_2023 = cr2met.tmax_1d_djf_30_40S().sel(time='2023').values


def tau(yr_list, init_parm):
    x, y = metrics.obs_data_tmax_1d_remove_year(yr_list)
    return metrics.tau_best_estimate(x, y, tglobal_2022, tlocal_2023,
                                     init_parm)


init_parms = [[37, 4, 2, 0.1],
              [37, 4, 2, 0.1],
              [37, 4, 2, 0.1],
              [36.5, 0.9, 1.2, 0.3]]

removed_years = [list(), [2017], [2023], [2017, 2023]]

best_estimates = [tau(years, init_parm)
                  for years, init_parm in zip(removed_years, init_parms)]

basedir = '/home/tcarrasco/result/data/bootstrap/'
cr2met = 'MLE_CR2MET_tmax_1d_30_40S_nboot_1000_gev_evaluation.nc'
no2017 = 'MLE_CR2MET_tmax_1d_30_40S_nboot_10_gev_no2017_evaluation.nc'
no2023 = 'MLE_CR2MET_tmax_1d_30_40S_nboot_10_gev_no2023_evaluation.nc'
no2017_no2023 = 'MLE_CR2MET_tmax_1d_30_40S_nboot_10_gev_' + \
    'no2017_no2023_evaluation.nc'

filenames = [cr2met, no2017, no2023, no2017_no2023]
models = [xr.open_dataset(join(basedir, filename)) for filename in filenames]
models = [metrics.bootstrap_tau_gev(model, tglobal_2022, tlocal_2023)
          for model in models]
model_names = ['CR2MET', 'No 2017', 'No 2023', 'No 2017 - No2023']


def retain_valid(x):
    # x[~np.isfinite(x)] = 1e10
    return x


tau_arrs = [retain_valid(m['tau'].values) for m in models]
center = [np.quantile(tau_arr, 0.5, axis=0) for tau_arr in tau_arrs]
lower = [np.quantile(tau_arr, 0.025, axis=0) for tau_arr in tau_arrs]
upper = [np.quantile(tau_arr, 0.975, axis=0) for tau_arr in tau_arrs]

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, ax = plt.subplots(1, 1, figsize=(12, 3))
varname = 'tau'

width = np.array(upper) - np.array(lower)
y_pos = np.arange(len(model_names))
barlist = ax.barh(y_pos, width=width, left=lower,
                  height=0.4, align='center')
colors = ['#3EC1D3', '#3EC1D3', '#3EC1D3', '#3EC1D3']
for bar, color in zip(barlist, colors):
    bar.set_color(color)
plt.scatter(best_estimates, y_pos, s=200, marker='|', color=[
            'k', 'k', 'k', 'k'], zorder=4)
plt.yticks(y_pos, model_names)
ax.set_axisbelow(True)
plt.grid(lw=0.4, ls='--', color='grey', zorder=-4)
plt.ylim([-0.5, 3.5])
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Actual return period')
ax.spines.right.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.top.set_visible(False)
ax.tick_params(direction="in")
ax.set_xscale('log')
plt.xlim([0.1, 1e9])
plt.xticks([0.1, 1.0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
plt.axvline(1, color='k', lw=1.0)
plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'MLE_tmax_1d_metrics_sensitivity.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
