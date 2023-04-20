import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum
from scipy.stats import norm
from scipy.stats import kstest

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402
from utilities import cr2met  # noqa: E402
from utilities import math as pmath  # noqa: E402

tlocal = cr2met.tmax_1d_djf_30_40S()
t2017 = tlocal.sel(time='2017').values
t2023 = tlocal.sel(time='2023').values
x, y = metrics.obs_data_tmax_1d_remove_year(tlocal_year_to_remove=[2017, 2023])
data = np.ravel(y)

# compute non parametric tau
u, tau = pmath.return_periods(data, method='up')

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# create figure
fig = plt.figure(figsize=(8, 6))

plt.scatter(tau, u, marker='o', facecolor='#65647C',
            edgecolor='#000000', alpha=0.7, label='CR2MET')

# set grid
plt.grid(lw=0.2, ls='--', color='grey')

# set x log scale
plt.gca().set_xscale('log')

# set ticks and lims
xticks = np.arange(1, 11, 1)
xticks = np.append(xticks, [xticks*z for z in [1e2, 1e3, 1e4]])
plt.axhline(t2017, c='r', lw=1.0, label='2017')
plt.axhline(t2023, c='b', lw=1.0, label='2023')
plt.xticks(xticks)
plt.xlim([0.9, 1000])
plt.ylim([30, 50])

# set title and labels
plt.xlabel('Return period (yr)')
plt.ylabel('Tmax (ºC)')

# set legend
plt.legend()


# set title and labels
basedir = '/home/tcarrasco/result/images/png/'
filename = 'CR2MET_return_period_raw.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
