import sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.ticker import FormatStrFormatter

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

import utilities.gmst as gmst  # noqa: E402

ds_hadcrut = gmst.annual_global_HadCRUT()
hadcrut_anom = ds_hadcrut['anom']
hadcrut_lower = ds_hadcrut['lower']
hadcrut_upper = ds_hadcrut['upper']
hadcrut_smooth = gmst.annual_global_HadCRUT_5year_smooth()

lens1 = gmst.annual_lens1_ensmean()
lens2 = gmst.annual_lens2_ensmean()

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, axs = plt.subplots(1, 1, figsize=(12, 7))

ax = axs
ax.fill_between(hadcrut_anom.time.dt.year, hadcrut_lower,
                hadcrut_upper, color='grey', alpha=0.7)
ax.plot(hadcrut_anom.time.dt.year, hadcrut_anom, c='k')
ax.plot(hadcrut_smooth.time.dt.year, hadcrut_smooth, lw=1.0, c='fuchsia')

ax.plot(lens1.time.dt.year, lens1, lw=1.0, ls='--', c='r')
ax.plot(lens2.time.dt.year, lens2, lw=1.0, ls='--', c='b')

ax.grid(c='grey', lw=0.5, ls='--', zorder=-4)
ax.set_axisbelow(True)
ax.set_xlabel('')
ax.set_ylabel('GMST (ºC)')

print('past-obs', hadcrut_smooth.sel(time=slice('1850', '1900')).mean('time'))
print('past-lens2', lens2.sel(time=slice('1850', '1900')).mean('time'))
print('pres-obs', hadcrut_smooth.sel(time=slice('2011', '2020')).mean('time'))
print('pres-lens1', lens1.sel(time=slice('2011', '2020')).mean('time'))
print('pres-lens2', lens2.sel(time=slice('2011', '2020')).mean('time'))

for i in range(lens1.size):
    if lens1[i:(i+20)].mean('time') >= 2.0:
        print(lens1[i:(i+20)])
        break
    
for i in range(lens2.size):
    if lens2[i:(i+20)].mean('time') >= 2.0:
        print(lens2[i:(i+20)])
        break

plt.tight_layout()
plt.savefig('/home/tcarrasco/result/images/png/GMST_obs_mod.png', dpi=300)
plt.show()
