import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from os.path import join

basedir = '/home/tcarrasco/result/data/all_estimate/'


cr2met = 'MLE_CR2MET_tmax_1d_30_40S_all_estimate_nboot_1000_gev_evaluation.csv'
lens1 = 'MLE_LENS1_tmax_1d_30_40S_all_estimate_nboot_100_gev_evaluation.csv'

filenames = [cr2met, lens1, cr2met, cr2met, cr2met]
models = [pd.read_csv(join(basedir, filename), index_col=0)
          for filename in filenames]
model_names = ['CR2MET', 'CESM1-LENS', 'CESM2-LENS', 'EC Earth', 'Model z']

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(4, 1, figsize=(8, 7.5))

varnames = ['mu0', 'sigma', 'alpha', 'eta']
xlims = [[34, 38], [0, 2], [-4, 4], [-1, 1]]
for varname, ax, xlim in zip(varnames, axs, xlims):
    center = [m.loc['Best estimate', varname] for m in models]
    lower = [m.loc['Upper estimate', varname] for m in models]
    upper = [m.loc['Lower estimate', varname] for m in models]
    width = np.array(upper) - np.array(lower)

    plt.sca(ax)
    y_pos = np.arange(len(model_names))
    barlist = ax.barh(y_pos, width=width, left=lower,
                      height=0.4, align='center')
    colors = ['#3EC1D3', 'grey', 'none', 'none', 'none']
    for bar, color in zip(barlist, colors):
        bar.set_color(color)
    plt.scatter(center, y_pos, s=80, marker='|', color=[
                'k', 'k', 'none', 'none', 'none'], zorder=4)
    plt.yticks(y_pos, model_names)
    plt.xlim(xlim)
    ax.set_axisbelow(True)
    plt.grid(lw=0.4, ls='--', color='grey', zorder=-4)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(varname)
    ax.tick_params(direction="in")

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'MLE_tmax_1d_validation_nboot_100.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
