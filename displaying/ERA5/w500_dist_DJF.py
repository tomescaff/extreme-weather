import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

basedir = '/home/tcarrasco/result/data/ERA5/w500_valley/final/'
filename = 'ERA5_w500_6h_1979_2023_valley_025deg_selpoint_merged.nc'

ds = xr.open_dataset(basedir + filename)

da = ds['w']
da_summer = da.where(da.time.dt.month.isin([12, 1, 2]), drop=True)
da_2017 = da_summer.sel(time='2017-01-26').max()
da_2019 = da_summer.sel(time='2019-02-03').max()
da_2023 = da_summer.sel(time='2023-02-03').max()
data = da_summer.values
p1p0 = np.quantile(data, 0.01*99)
p2p0 = np.quantile(data, 0.01*98)


# compute histogram
hist, bins = np.histogram(data, np.linspace(-2.5, 1.5, 50), density=True)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 8
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig = plt.figure()
# plot the histogram
fullwidth = (bins[1] - bins[0])
width = 0.85 * fullwidth
center = (bins[:-1] + bins[1:]) / 2

plt.bar(center, (hist > 0)*3.0, align='center', width=fullwidth,
        edgecolor='none', facecolor='lightgrey', alpha=0.7, lw=0.2)

plt.bar(center, hist, align='center', width=width, edgecolor='#000000',
        facecolor='#65647C', alpha=1.0, lw=0.2)

plt.axvline(da_2017.values, color='red', lw=1, label='2017 event')
plt.axvline(da_2019.values, color='green', lw=1, label='2019 event')
plt.axvline(da_2023.values, color='blue', lw=1, label='2023 event')
plt.axvline(p1p0, color='k', lw=0.5, ls='--', label='p1%')
plt.axvline(p2p0, color='k', lw=0.5, ls='dotted', label='p2%')

plt.xlim([-2.5, 1.5])
plt.ylim([0, 3.0])
plt.ylabel('PDF')
plt.xlabel('W500 hPa (Pa/s) [36ºS, 72ºW]')
plt.legend()

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_w500_valley_dist.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
