import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

bdir = '/home/tcarrasco/result/data/ERA5/t_vertical_profile/'

t2m = xr.open_mfdataset(bdir + 'ERA5_t2m_6h_2017_*_Global_025deg-fldmax.nc')
t925 = xr.open_mfdataset(bdir + 'ERA5_t925_6h_2017_*_Global_025deg-fldmax.nc')
t750 = xr.open_mfdataset(bdir + 'ERA5_t750_6h_2017_*_Global_025deg-fldmax.nc')
t500 = xr.open_mfdataset(bdir + 'ERA5_t500_6h_2017_*_Global_025deg-fldmax.nc')
t300 = xr.open_mfdataset(bdir + 'ERA5_t300_6h_2017_*_Global_025deg-fldmax.nc')

theta1000 = t2m['t2m']
theta925 = t925['t']*(1000/925)**0.286
theta750 = t925['t']*(1000/750)**0.286
theta500 = t925['t']*(1000/500)**0.286
theta300 = t925['t']*(1000/300)**0.286

plev = np.array([1000, 925, 750, 500, 300])
time = theta1000.time
nlev = plev.size
ntime = time.size
data = np.zeros((nlev, ntime))*np.nan
data[0, :] = theta1000.values
data[1, :] = theta925.values
data[2, :] = theta750.values
data[3, :] = theta500.values
data[4, :] = theta300.values

# z1-z0 = 8*np.log(1000/p1)
z = 7000*np.log(1000/plev)
x = np.arange(ntime)
# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
fig = plt.figure(figsize=(12, 8))
cs = plt.contour(x, z, data, levels=np.arange(280, 430, 15), colors='k',
                 linewidths=0.8)
plt.yticks(z, plev)
xticks = x[::8]
xlabels = [f'2017-{t.dt.month.values:02}-{t.dt.day.values:02}'
           for t in time[::8]]
plt.xticks(xticks, xlabels, rotation=90)
plt.ylabel('Pressure level (hPa)')
plt.clabel(cs, cs.levels, inline=True, fontsize=8)
plt.title('Potential temperature (K) at (-36ºS, -72ºW)')

basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_theta_vertical_profile_2017.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
