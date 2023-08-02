import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import sys
import cmaps

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing')  # noqa: E402

import utilities.qgdynamics as qg

year = '2023'

if year == '2017':
    ida = 24*4
    idb = 26*4
else:
    ida = (24+8)*4
    idb = (26+8)*4

basedir = '/home/tcarrasco/result/data/ERA5/uvT/'
filename = 'uvT.nc'
ds = xr.open_dataset(basedir+filename).sel(time=year)
ua500 = ds['u'].sel(latitude=-36, longitude=-72, level=500)
ua700 = ds['u'].sel(latitude=-36, longitude=-72, level=700)
ua925 = ds['u'].sel(latitude=-36, longitude=-72, level=925)
va500 = ds['v'].sel(latitude=-36, longitude=-72, level=500)
va700 = ds['v'].sel(latitude=-36, longitude=-72, level=700)
va925 = ds['v'].sel(latitude=-36, longitude=-72, level=925)
ta = ds['t'].sel(latitude=-36, longitude=-72)

filename = 'zw.nc'
ds = xr.open_dataset(basedir+filename).sel(time=year)
z = ds['z'].sel(latitude=-36, longitude=-72, level=500)/9.8
om = ds['w'].sel(latitude=-36, longitude=-72, level=700)

filename = 'slp_30S_72W.nc'
ds = xr.open_dataset(basedir+filename).sel(time=year)
slpn = ds['msl'].sel(latitude=-30, longitude=-72)

filename = 'slp_40S_74W.nc'
ds = xr.open_dataset(basedir+filename).sel(time=year)
slps = ds['msl'].sel(latitude=-40, longitude=-74)

basedir = '/home/tcarrasco/result/data/ERA5/u_10m_spamin/final/'
filename = 'ERA5_u10_6h_1979_2023_36_38S_preAndes_025deg_spamin_merged.nc'
ds = xr.open_dataset(basedir + filename)
puelche = ds['u10'].sel(time=slice(year+'-01-01', year+'-02-28'))

basedir = '/home/tcarrasco/result/data/ERA5/v_10m_spamax/final/'
filename = 'ERA5_v10_6h_1979_2023_36_38S_coast_025deg_spamax_merged.nc'
ds = xr.open_dataset(basedir + filename)
surazo = ds['v10'].sel(time=slice(year+'-01-01', year+'-02-28'))

time = puelche.time
ntime = time.size

x = np.arange(ntime)
# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 10

levels = np.arange(-27.5, 32.5, 5)

fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

###

host = axs[0]
ax2 = host.twinx()
ax3 = host.twinx()

host.set_ylim(5500, 6000)
ax2.set_ylim(-2, 2)
ax3.set_ylim(-1250, 1250)

host.axvspan(x[ida], x[idb], alpha=0.5, color='grey')
ax2.axhline(0, color='k', lw=1, ls='--')

host.set_ylabel("Z500 hPa (gpm) [-36ºS, -72ºW]")
ax2.set_ylabel("Omega500 hPa (Pa/s) [-36ºS, -72ºW]")
ax3.set_ylabel("dp/dy")

p1 = host.plot(x, z, color='k', label="Z500")
p2 = ax2.plot(x, om, color='b', label="w700")
p3 = ax3.plot(x, slpn - slps, color='r', label="dp/dy")

host.legend(handles=p1+p2+p3, loc='upper left')
ax3.spines['right'].set_position(('outward', 60))

host.yaxis.label.set_color(p1[0].get_color())
ax2.yaxis.label.set_color(p2[0].get_color())
ax3.yaxis.label.set_color(p3[0].get_color())

###

host = axs[1]
ax2 = host.twinx()
ax3 = host.twinx()

host.set_ylim(-32, 32)
ax2.set_ylim(-9, 9)
ax3.set_ylim(-5.5, 5.5)

host.axvspan(x[ida], x[idb], alpha=0.5, color='grey')
host.axhline(0, color='k', lw=1, ls='--')
host.set_ylabel("u500 hPa (m/s) [-36ºS, -72ºW]")
ax2.set_ylabel("u925 hPa (m/s) [-36ºS, -72ºW]")
ax3.set_ylabel("puelche")

p1 = host.plot(x, ua500, color='k', label="u500")
p2 = ax2.plot(x, ua925, color='b', label="u920")
p3 = ax3.plot(x, puelche, color='r', label="puelche")

host.legend(handles=p1+p2+p3, loc='upper left')
ax3.spines['right'].set_position(('outward', 60))

host.yaxis.label.set_color(p1[0].get_color())
ax2.yaxis.label.set_color(p2[0].get_color())
ax3.yaxis.label.set_color(p3[0].get_color())

###

host = axs[2]
ax2 = host.twinx()
ax3 = host.twinx()

host.set_ylim(-22, 22)
ax2.set_ylim(-22, 22)
ax3.set_ylim(-18, 18)

host.axvspan(x[ida], x[idb], alpha=0.5, color='grey')
host.axhline(0, color='k', lw=1, ls='--')

host.set_ylabel("v500 hPa (m/s) [-36ºS, -72ºW]")
ax2.set_ylabel("v925 hPa (m/s) [-36ºS, -72ºW]")
ax3.set_ylabel("surazo")

p1 = host.plot(x, va500, color='k', label="v500")
p2 = ax2.plot(x, va925, color='b', label="v920")
p3 = ax3.plot(x, surazo, color='r', label="surazo")

host.legend(handles=p1+p2+p3, loc='upper left')
ax3.spines['right'].set_position(('outward', 60))

host.yaxis.label.set_color(p1[0].get_color())
ax2.yaxis.label.set_color(p2[0].get_color())
ax3.yaxis.label.set_color(p3[0].get_color())

###

host = axs[3]
ax2 = host.twinx()
ax3 = host.twinx()

host.set_ylim(-0.008, 0.008)
ax2.set_ylim(-0.008, 0.008)
ax3.set_ylim(-0.008, 0.008)

host.axvspan(x[ida], x[idb], alpha=0.5, color='grey')
host.axhline(0, color='k', lw=1, ls='--')

host.set_ylabel("du 500-925 hPa (m/s) [-36ºS, -72ºW]")
ax2.set_ylabel("dv 500-925 hPa (m/s) [-36ºS, -72ºW]")
ax3.set_ylabel("T1 + T2")

# Algunas constantes y f
g = 9.8  # gravity constant
R = 6400000  # Earth radius
omega = 2 * np.pi / (24 * 60 * 60)
B = 2 * omega * np.cos(np.deg2rad(-36)) / R
Lx = 10*1e3
Ly = 10*1e3
k = 2*np.pi/Lx
m = 2*np.pi/Ly

t1 = -va700*(ua500 - ua925)/((500-925)*100)
t2 = ua700*(va500 - va925)/((500-925)*100)
t3 = B/(k**2+m**2)*(va500 - va925)/((500-925)*100)
p1 = host.plot(x, t1, color='k', label="-vdu/dp")
p2 = ax2.plot(x, t2, color='b', label="udv/dp")
p3 = ax3.plot(x, t1+t2+t3, color='r', label="T1+T2+T3")

host.legend(handles=p1+p2+p3, loc='upper left')
ax3.spines['right'].set_position(('outward', 60))

host.yaxis.label.set_color(p1[0].get_color())
ax2.yaxis.label.set_color(p2[0].get_color())
ax3.yaxis.label.set_color(p3[0].get_color())

plt.sca(axs[3])
xticks = x[::8]
xlabels = [f'{year}-{t.dt.month.values:02}-{t.dt.day.values:02}'
           for t in time[::8]]
plt.xticks(xticks, xlabels, rotation=90)

plt.tight_layout()
basedir = '/home/tcarrasco/result/images/png/'
filename = 'ERA5_timeseries_'+year+'.png'
filepath = basedir + filename
plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
