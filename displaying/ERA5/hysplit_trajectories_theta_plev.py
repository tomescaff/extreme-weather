import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


def termodynamic_to_potential(tt, plev):
    return tt*(1000/plev)**0.286


def potential_to_termodynamic(th, plev):
    return th*(1000/plev)**-0.286


def plev_to_std_height(plev):
    return 7000*np.log(1000/plev)


basedir = '/home/tcarrasco/result/data/HYSPLIT/'

# hysplit traj 2017
filename = 'retro_26Jan17_12Z.txt'
filepath = basedir + filename
df = pd.read_csv(filepath, skiprows=7, header=None, sep='\s+')  # noqa: W605
tt17 = df.loc[:, 14].values  # termodinamic temperature
th17 = df.loc[:, 13].values  # potential temperature
p17 = df.loc[:, 12].values  # pressure levels
z17 = df.loc[:, 11].values  # standard height

# selected points at 00:00:00 Z
sel_tt17 = df.loc[(df[5] == 0), 14].values
sel_th17 = df.loc[(df[5] == 0), 13].values
sel_p17 = df.loc[(df[5] == 0), 12].values
sel_z17 = df.loc[(df[5] == 0), 11].values

# hysplit traj 2023
filename = 'retro_03Feb23_12Z.txt'
filepath = basedir + filename
df = pd.read_csv(filepath, skiprows=7, header=None, sep='\s+')  # noqa: W605
tt23 = df.loc[:, 14].values
th23 = df.loc[:, 13].values
p23 = df.loc[:, 12].values
z23 = df.loc[:, 11].values

# selected points at 00:00:00 Z
sel_tt23 = df.loc[(df[5] == 0), 14].values
sel_th23 = df.loc[(df[5] == 0), 13].values
sel_p23 = df.loc[(df[5] == 0), 12].values
sel_z23 = df.loc[(df[5] == 0), 11].values

# data for analysis

df = pd.DataFrame(columns=['2017', '2023'])

df.loc['z init (m)'] = [sel_z17[0], sel_z23[0]]
df.loc['p init (hPa)'] = [sel_p17[0], sel_p23[0]]
df.loc['th init (K)'] = [sel_th17[0], sel_th23[0]]
df.loc['tt init (K)'] = [sel_tt17[0], sel_tt23[0]]

df.loc['z end (m)'] = [z17[0], z23[0]]
df.loc['p end (hPa)'] = [p17[0], p23[0]]
df.loc['th end (K)'] = [th17[0], th23[0]]
df.loc['tt end (K)'] = [tt17[0], tt23[0]]

df.loc['Dz (m)'] = [z17[0]-sel_z17[0], z23[0]-sel_z23[0]]
df.loc['Dp (hPa)'] = [p17[0]-sel_p17[0], p23[0]-sel_p23[0]]
df.loc['Dth (K)'] = [th17[0]-sel_th17[0], th23[0]-sel_th23[0]]
df.loc['Dtt (K)'] = [tt17[0]-sel_tt17[0], tt23[0]-sel_tt23[0]]
df.loc['Dtt/Dt (K/s)'] = df.loc['Dtt (K)'].values/(12*3600)
df.loc['w (m/s)'] = df.loc['Dz (m)'].values/(12*3600)
df.loc['omega (Pa/s)'] = df.loc['Dp (hPa)'].values/(12*3600)*100

df['Diff 2017-2023'] = df['2017'] - df['2023']

df.to_csv(basedir + 'traj_analysis.csv')

# vertical profile

filepath = '/home/tcarrasco/result/data/ERA5/uvT/uvT.nc'
t = xr.open_mfdataset(filepath)
t = t.sel(latitude=-36.5, longitude=-72.0, level=slice(500, 1000))
vp_p = t.level.values
vp_z = plev_to_std_height(vp_p)
vp_tt17 = t['t'].sel(time='2017-01-26 12:00:00').squeeze().values
vp_tt23 = t['t'].sel(time='2023-02-03 12:00:00').squeeze().values
vp_th17 = termodynamic_to_potential(vp_tt17, vp_p)
vp_th23 = termodynamic_to_potential(vp_tt23, vp_p)

# yticks
lticks = np.array([1000, 925, 850, 700, 500, 300])
hticks = plev_to_std_height(lticks)

# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10
fig = plt.figure(figsize=(6, 8))
plt.plot(vp_th17, vp_z, color='r', lw=0.8, ls='--', label='Traj 2017')
plt.plot(vp_th23, vp_z, color='b', lw=0.8, ls='--', label='Traj 2023')
plt.plot(th17, z17, color='r', lw=1.2)
plt.plot(th23, z23, color='b', lw=1.2)
plt.scatter(sel_th23, sel_z23, color='b', s=10)
plt.scatter(sel_th17, sel_z17, color='r', s=10)
plt.scatter(th23[0], z23[0], color='b', s=15, marker='*')
plt.scatter(th17[0], z17[0], color='r', s=15, marker='*')
plt.legend()
plt.ylabel('Pressure level (hPa)')
plt.xlabel('Potential temperature (K)')
plt.title('Vertical profile at [-36.5ºS, -72ºW]')
plt.yticks(hticks, lticks)
plt.ylim([hticks[0], hticks[-2]])
basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_hysplit_traj.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300)
