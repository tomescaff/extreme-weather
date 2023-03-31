import sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from scipy.stats import genextreme as gev

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import cr2met  # noqa: E402
from utilities import gmst  # noqa: E402
from utilities import math as pmath  # noqa: E402

tglobal = gmst.annual_5year_smooth()
tlocal = cr2met.tmax_1d_djf_30_40S()

x_prev = tglobal.sel(time=slice('1959', '1978'))
y_prev = tlocal.sel(time=slice('1960', '1979'))

x = tglobal.sel(time=slice('1979', '2022'))
y = tlocal.sel(time=slice('1980', '2023'))

init_params = [37, 4, 2, 0.1, 0.0]
mu0, sigma0, alpha, beta, eta = pmath.mle_gev_2d(
    y.values, x.values, init_params)

mu = mu0 + alpha*x
sigma = sigma0 + beta*x
mu_plus_1sigma = mu + sigma
mu_plus_2sigma = mu + 2*sigma
val_tau_10 = gev.isf(1/10, eta, mu, sigma)
val_tau_100 = gev.isf(1/100, eta, mu, sigma)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig = plt.figure(figsize=(8, 5))
plt.scatter(x_prev, y_prev, s=20, marker='o',
            edgecolor='#222831', facecolor='#EEEEEE', alpha=0.8)
plt.scatter(x, y, s=20, marker='o', edgecolor='#222831',
            facecolor='#00ADB5', alpha=0.8)

for year in [2017, 2019, 2023]:
    plt.text(x.sel(time=f'{year-1}')+0.01,
             y.sel(time=f'{year}'), f'{year}', fontsize=7)

plt.plot(x, mu, c='#FF2E63', lw=1.5, label='Mean')
plt.plot(x, mu_plus_1sigma, c='#FF2E63', lw=0.5)
plt.plot(x, mu_plus_2sigma, c='#FF2E63', lw=0.5)
plt.plot(x, val_tau_100, c='#FF9A00', lw=1.5, label='100-year event')
plt.plot(x, val_tau_10, c='#FF9A00', lw=1.5, ls='--', label='10-year event')
plt.ylim([35, 43])
plt.xlim([-0.2, 1.0])
plt.grid(color='grey', lw=0.4, ls='--')
ax = plt.gca()
ax.tick_params(direction="in")
plt.xlabel('Global mean surface temperature anomaly (smoothed) [ºC]')
plt.ylabel('Tmax [DJF, 30-40ºS] (ºC)')
plt.legend(loc='upper center', ncol=3)
plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/CR2MET_tmax_1d_GMST_varsig.png',
            dpi=300)
plt.show()
