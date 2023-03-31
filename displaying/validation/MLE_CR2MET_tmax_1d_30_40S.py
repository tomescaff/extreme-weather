import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from os.path import join

basedir = '/home/tcarrasco/result/data/bootstrap/'

filename = 'MLE_CR2MET_tmax_1d_30_40S_nboot_100_gev_evaluation.nc'
cr2met = xr.open_dataset(join(basedir, filename))

# filename = 'MLE_tasmax_jan_LENS1_GMST_100_normal_validation_QN_NN.nc'
# lens1 = xr.open_dataset(join(basedir, filename))

# filename = 'MLE_tasmax_jan_LENS2_GMST_100_normal_validation_QN_NN.nc'
# lens2 = xr.open_dataset(join(basedir, filename))

model_names = ['CR2MET', 'CESM1-LENS', 'Model 2', 'Model 3', 'Model 4']
models = [cr2met, cr2met, cr2met, cr2met, cr2met]

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
    center = [np.quantile(m[varname].values, 0.5, axis=0) for m in models]
    lower = [np.quantile(m[varname].values, 0.025, axis=0) for m in models]
    upper = [np.quantile(m[varname].values, 0.975, axis=0) for m in models]
    width = np.array(upper) - np.array(lower)

    plt.sca(ax)
    y_pos = np.arange(len(model_names))

    barlist = ax.barh(y_pos, width=width, left=lower,
                      height=0.4, align='center')
    colors = ['#3EC1D3', 'none', 'none', 'none', 'none']
    for bar, color in zip(barlist, colors):
        bar.set_color(color)
    plt.scatter(center, y_pos, s=200, marker='|', color=[
                'k', 'none', 'none', 'none', 'none'], zorder=4)
    plt.yticks(y_pos, model_names)
    plt.xlim(xlim)
    ax.set_axisbelow(True)
    plt.grid(lw=0.4, ls='--', color='grey', zorder=-4)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(varname)
    ax.tick_params(direction="in")

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_tmax_1d_validation_nboot_100.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
