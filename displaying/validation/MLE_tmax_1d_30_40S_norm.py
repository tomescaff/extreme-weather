import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from os.path import join

basedir = '/home/tcarrasco/result/data/all_estimate/'


cr2met = 'MLE_CR2MET_tmax_1d_30_40S_all_estimate_nboot_1000_norm_' +\
    'no2017_no2023_evaluation.csv'
lens1 = 'MLE_LENS1_tmax_1d_30_40S_all_estimate_nboot_1000_' +\
    'tau_100_norm_evaluation.csv'
lens2 = 'MLE_LENS2_tmax_1d_30_40S_all_estimate_nboot_1000_' +\
    'tau_100_norm_evaluation.csv'

filenames = [cr2met, lens1, lens2, cr2met, cr2met]
models = [pd.read_csv(join(basedir, filename), index_col=0)
          for filename in filenames]
model_names = ['CR2MET', 'CESM1-LENS', 'CESM2-LENS', 'EC Earth 3', 'Model z']

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'arial'

fig, axs = plt.subplots(3, 1, figsize=(8, 7.5))

varnames = ['mu0', 'sigma', 'alpha']
xlabels = [r'Location parameter: $\mu_0$ (ºC)',
           r'Scale parameter: $\sigma$ (ºC)',
           r'Trend parameter: $\alpha$ (ºC/ºC)']
xlims = [[34.5, 38.5], [0, 2], [-4, 4]]
for varname, ax, xlim, xlabel in zip(varnames, axs, xlims, xlabels):
    center = [m.loc['Best estimate', varname] for m in models]
    lower = [m.loc['Upper estimate', varname] for m in models]
    upper = [m.loc['Lower estimate', varname] for m in models]
    width = np.array(upper) - np.array(lower)

    plt.sca(ax)
    y_pos = np.arange(len(model_names))
    barlist = ax.barh(y_pos, width=width, left=lower,
                      height=0.4, align='center')
    colors = ['#3EC1D3', 'grey', 'grey', 'none', 'none']
    for bar, color in zip(barlist, colors):
        bar.set_color(color)
    plt.scatter(center, y_pos, s=100, marker='|', color=[
                'k', 'k', 'k', 'none', 'none'], zorder=4)
    plt.yticks(y_pos, model_names)
    plt.xlim(xlim)
    ax.set_axisbelow(True)
    plt.grid(lw=0.4, ls='--', color='grey', zorder=-4)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(xlabel)
    ax.tick_params(direction="in")

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'MLE_tmax_1d_30_40S_validation_nboot_1000_norm.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
