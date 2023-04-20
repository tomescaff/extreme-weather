import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum
from scipy.stats import norm
from scipy.stats import kstest

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import lens  # noqa: E402
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402


tlocal = lens.lens1_tmax_1d_djf_30_40S_40m()
tanom = tlocal - tlocal.mean('ensemble')
data = np.ravel(tanom.values)

fit_nor = norm.fit(data)
fit_gev = gev.fit(data)
fit_gum = gum.fit(data)

# compute non parametric tau
u, tau = pmath.return_periods(data, method='up')

xmin, xmax = -10, 20

# computing best x ticks
y = np.linspace(xmin, xmax, 1000)
x = 1/norm.sf(y, *fit_nor)

# computing y values
y_norm = norm.isf(1/x, *fit_nor)
y_gev = gev.isf(1/x, *fit_gev)
y_gum = gum.isf(1/x, *fit_gum)


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
            edgecolor='#000000', alpha=0.7, label='LENS1 control run')

# plot the parametric curves
plt.plot(x, y_norm, color='#0B2447', lw=1.5, alpha=1, label='Normal')
plt.plot(x, y_gev, color='#159895', lw=1.5, alpha=1, label='GEV')
plt.plot(x, y_gum, color='#FC2947', lw=1.5, alpha=1, label='Gumbel')

# set grid
plt.grid(lw=0.2, ls='--', color='grey')

# set x log scale
plt.gca().set_xscale('log')

# set ticks and lims

xticks = np.arange(1, 11, 1)
xticks = np.append(xticks, [xticks*z for z in [1e2, 1e3, 1e4]])
plt.xticks(xticks)
plt.xlim([0.9, 60000])
plt.ylim([xmin, xmax])

# set title and labels
plt.xlabel('Return period (yr)')
plt.ylabel('Tmax (ºC)')

# set legend
plt.legend()


# set title and labels
basedir = '/home/tcarrasco/result/images/png/'
filename = 'LENS1_ensanom_return_period.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
# plt.show()
