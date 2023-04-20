import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from os.path import join

basedir = '/home/tcarrasco/result/data/all_estimate/'

lens1 = 'MLE_LENS1_tmax_1d_30_40S_all_estimate_nboot_100_gev_evaluation.csv'

filenames = [lens1, lens1, lens1, lens1, lens1, lens1, lens1, lens1]
models = [pd.read_csv(join(basedir, filename), index_col=0)
          for filename in filenames]
model_names = ['CESM1-LENS Method #1',
               'CESM1-LENS Method #2',
               'CESM2-LENS Method #1',
               'CESM2-LENS Method #2',
               'EC Earth Method #1',
               'EC Earth Method #2',
               'Model z Method #1',
               'Model z Method #2']

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(4, 1, figsize=(8, 10))

varnames = ['tau_pa', 'tau_ac', 'PR ac-pa', 'Delta ac-pa']
xlabels = ['Counterfactural return period (yr)', 'Factual return period (yr)',
           'Historical probability ratio', 'Historical intesity change (ºC)']
xlims = [[0.1, 10000], [0.1, 10000], [0.1, 10000], [-1.5, 1.5]]
for varname, ax, xlim, xlabel in zip(varnames, axs, xlims, xlabels):
    center = [m.loc['Best estimate', varname] for m in models]
    lower = [m.loc['Upper estimate', varname] for m in models]
    upper = [m.loc['Lower estimate', varname] for m in models]
    width = np.array(upper) - np.array(lower)

    plt.sca(ax)

    y_pos = np.arange(len(model_names))
    barlist = ax.barh(y_pos, width=width, left=lower,
                      height=0.4, align='center')
    colors = ['#3EC1D3', '#3EC1D3', 'none',
              'none', 'none', 'none', 'none', 'none']
    for bar, color in zip(barlist, colors):
        bar.set_color(color)
    ax.scatter(center, y_pos, s=80, marker='|', color=[
        'k', 'k', 'none', 'none', 'none', 'none', 'none', 'none'], zorder=4)
    ax.set_yticks(y_pos, model_names)
    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_axisbelow(True)
    ax.grid(lw=0.4, ls='--', color='grey', zorder=-4)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(xlabel)
    # ax.tick_params(direction="in")

    if varname != 'Delta ac-pa':
        # xticks = np.arange(1, 11, 1)
        # xticks = np.append(xticks, [xticks*z for z in [1e1, 1e2, 1e3, 1e4]])
        ax.set_xscale('log')
        # ax.set_xticks(xticks)

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'MLE_tmax_1d_metrics_historical_nboot_100.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
