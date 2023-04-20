import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from os.path import join

basedir = '/home/tcarrasco/result/data/bootstrap/'

cr2met = 'MLE_CR2MET_tmax_1d_30_40S_nboot_1000_gev_evaluation.nc'
no2017 = 'MLE_CR2MET_tmax_1d_30_40S_nboot_1000_gev_no2017_evaluation.nc'
no2023 = 'MLE_CR2MET_tmax_1d_30_40S_nboot_1000_gev_no2023_evaluation.nc'
no2017_no2023 = 'MLE_CR2MET_tmax_1d_30_40S_nboot_1000_gev_' + \
    'no2017_no2023_evaluation.nc'
lens1 = 'MLE_LENS1_tmax_1d_30_40S_nboot_100_gev_evaluation.nc'
lens1_val = 'MLE_LENS1_tmax_1d_30_40S_nboot_100_gev_validation.nc'
lens1_1980_2023 = 'MLE_LENS1_tmax_1d_30_40S_nboot_100_gev_1980_2023.nc'

filenames = [cr2met, no2017, no2023, no2017_no2023, lens1, lens1_val,
             lens1_1980_2023]
models = [xr.open_dataset(join(basedir, filename)) for filename in filenames]
model_names = ['CR2MET', 'No 2017', 'No 2023', 'No 2017 - No2023',
               'LENS1 (1921-2100)', 'LENS1 BC (1980-1923)',
               'LENS1 (1980-2023)']


# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(4, 1, figsize=(8, 8))

varnames = ['mu0', 'sigma', 'alpha', 'eta']
xlims = [[34, 38], [0, 2], [-4, 4], [-1, 1]]
for varname, ax, xlim in zip(varnames, axs, xlims):
    center = [np.quantile(m[varname].values, 0.5, axis=0) for m in models]
    lower = [np.quantile(m[varname].values, 0.025, axis=0) for m in models]
    upper = [np.quantile(m[varname].values, 0.975, axis=0) for m in models]
    width = np.array(upper) - np.array(lower)

    plt.sca(ax)
    y_pos = np.arange(len(model_names))

    barlist = ax.barh(y_pos, width=width, left=lower,
                      height=0.4, align='center')
    colors = ['#3EC1D3', '#3EC1D3', '#3EC1D3', '#3EC1D3', 'grey', 'grey',
              'grey']
    for bar, color in zip(barlist, colors):
        bar.set_color(color)
    plt.scatter(center, y_pos, s=50, marker='|', color=[
                'k', 'k', 'k', 'k', 'k', 'k', 'k'], zorder=4)
    plt.yticks(y_pos, model_names)
    plt.xlim(xlim)
    ax.set_axisbelow(True)
    plt.grid(lw=0.4, ls='--', color='grey', zorder=-4)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(varname)
    ax.tick_params(direction="in")

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'MLE_tmax_1d_validation_nboot_sensitivity.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
