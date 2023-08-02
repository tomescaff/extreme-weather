import sys
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

import utilities.stations as stns  # noqa: E402


def annual_cycle(stn):
    stn_1991_2020 = stn.sel(time=slice('1991', '2020'))

    # complete data
    dr = pd.date_range('1992-01-01', '1992-12-31', freq='1d')
    n = dr.size
    N = 365
    x = np.zeros((N,))*np.nan

    k = 0
    for i in range(n):
        month = dr[i].month
        day = dr[i].day
        if month == 2 and day == 29:
            continue
        else:
            dayclim = np.zeros((30,))*np.nan
            for j, year in enumerate(np.arange(1991, 2021)):
                try:
                    dayval = stn_1991_2020.sel(time=f'{year}-{month}-{day}')
                except Exception as e:
                    continue
                dayclim[j] = dayval
            x[k] = np.nanmean(dayclim)
            k = k + 1

    yt = np.zeros([N, 1])
    n = len(x)
    for k in range(4):
        A = [0]
        B = [0]
        for t in range(n):
            # ecuaciones 9.60a y 9.60b Wilks
            A[0] = A[0] + (2/n) * x[t]*np.cos((2*np.pi*(k+1)*(t+1))/n)
            B[0] = B[0] + (2/n) * x[t]*np.sin((2*np.pi*(k+1)*(t+1))/n)

        for t in range(n):
            # ecuación 9.62b (sin promedio)
            yt[t, 0] = yt[t, 0] + (A[0]*np.cos((2*np.pi*(k+1)*(t+1))/n) +
                                   B[0]*np.sin((2*np.pi*(k+1)*(t+1))/n))

    yt = yt + np.mean(x)
    annual_cycle = x
    annual_cycle_4harms = yt
    return annual_cycle, annual_cycle_4harms


# Add every font at the specified location
font_dir = ['/home/tcarrasco/result/fonts/Merriweather',
            '/home/tcarrasco/result/fonts/arial']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
plt.rcParams["font.family"] = 'arial'
plt.rcParams["font.size"] = '10'


# heatwave curico
fp_p90 = '/home/tcarrasco/result/data/CU/' +\
         'UmbralesdeOlasdeCalor(Diurna)_2023-06-20_23_18.csv'
df_p90 = pd.read_csv(fp_p90, sep=';')
p90_ene = df_p90.loc[:, 'Ene'].values
p90_feb = df_p90.loc[:, 'Feb'].values
x = stns.cu_tmax_daily_1958_2023()
ac, ac4h = annual_cycle(x)
dr = pd.date_range('1993-01-01', '1994-12-31', freq='1d')
da_ac4h = xr.DataArray(np.append(ac4h, ac4h),
                       coords=[dr],
                       dims=['time'])


# heatwave curico 2017-01-26
p90 = np.append(p90_ene, p90_feb)[10:(10+31)]
mindate = '01-11'
maxdate = '02-10'
xsel = x.sel(time=slice('2017-'+mindate, '2017-'+maxdate)).values
ac4hsel = da_ac4h.sel(time=slice('1994-'+mindate, '1994-'+maxdate)).values
t = np.arange(xsel.size)
fig = plt.figure(figsize=(12, 4))
plt.fill_between(t, ac4hsel, xsel, where=xsel > ac4hsel,
                 interpolate=True, color='gold')
plt.fill_between(t, xsel, ac4hsel, where=xsel <= ac4hsel,
                 interpolate=True, color='royalblue')
plt.plot(t, xsel, color='k', lw=0.5, marker='o', markersize=3)
plt.plot(t, ac4hsel, color='grey', lw=0.8)
plt.plot(t, p90, color='r', lw=1.2, ls='--', label='90-percentile')
plt.xlim([0, 30])
plt.xticks([0, 7, 15, 23, 30], ['2017-01-11',
                                '2017-01-18',
                                '2017-01-26',
                                '2017-02-03',
                                '2017-02-10'],
           rotation=20)
plt.legend()
plt.ylabel('Daily maximum temperature (ºC)')
plt.ylim([20, 40])
plt.scatter(15, xsel[15], color='fuchsia', s=50, marker='*', zorder=5)
plt.grid(ls='--', color='gray', lw=0.5, axis='x')
basedir = '/home/tcarrasco/result/images/png/'
filename = 'heatwave_CU_2017_01_26.png'
plt.savefig(basedir + filename, dpi=300)


# heatwave curico 2023-02-03
p90 = np.append(p90_ene, p90_feb)[18:(18+31)]
mindate = '01-19'
maxdate = '02-18'
xsel = x.sel(time=slice('2023-'+mindate, '2023-'+maxdate)).values
ac4hsel = da_ac4h.sel(time=slice('1994-'+mindate, '1994-'+maxdate)).values
t = np.arange(xsel.size)
fig = plt.figure(figsize=(12, 4))
plt.fill_between(t, ac4hsel, xsel, where=xsel > ac4hsel,
                 interpolate=True, color='gold')
plt.fill_between(t, xsel, ac4hsel, where=xsel <= ac4hsel,
                 interpolate=True, color='royalblue')
plt.plot(t, xsel, color='k', lw=0.5, marker='o', markersize=3)
plt.plot(t, ac4hsel, color='grey', lw=0.8)
plt.plot(t, p90, color='r', lw=1.2, ls='--', label='90-percentile')
plt.xlim([0, 30])
plt.xticks([0, 7, 15, 23, 30], ['2023-01-19',
                                '2023-01-26',
                                '2023-02-03',
                                '2023-02-11',
                                '2023-02-18'],
           rotation=20)
plt.legend()
plt.ylabel('Daily maximum temperature (ºC)')
plt.ylim([20, 40])
plt.scatter(15, xsel[15], color='fuchsia', s=50, marker='*', zorder=5)
plt.grid(ls='--', color='gray', lw=0.5, axis='x')
basedir = '/home/tcarrasco/result/images/png/'
filename = 'heatwave_CU_2023_02_03.png'
plt.savefig(basedir + filename, dpi=300)


# heatwave chillan
fp_p90 = '/home/tcarrasco/result/data/CH/' +\
         'UmbralesdeOlasdeCalor(Diurna)_2023-06-27_18_31.csv'
df_p90 = pd.read_csv(fp_p90, sep=';')
p90_ene = df_p90.loc[:, 'Ene'].values
p90_feb = df_p90.loc[:, 'Feb'].values
x = stns.ch_tmax_daily_1960_2023()
ac, ac4h = annual_cycle(x)
dr = pd.date_range('1993-01-01', '1994-12-31', freq='1d')
da_ac4h = xr.DataArray(np.append(ac4h, ac4h),
                       coords=[dr],
                       dims=['time'])


# heatwave chillan 2017-01-26
p90 = np.append(p90_ene, p90_feb)[10:(10+31)]
mindate = '01-11'
maxdate = '02-10'
xsel = x.sel(time=slice('2017-'+mindate, '2017-'+maxdate)).values
ac4hsel = da_ac4h.sel(time=slice('1994-'+mindate, '1994-'+maxdate)).values
t = np.arange(xsel.size)
fig = plt.figure(figsize=(12, 4))
plt.fill_between(t, ac4hsel, xsel, where=xsel > ac4hsel,
                 interpolate=True, color='gold')
plt.fill_between(t, xsel, ac4hsel, where=xsel <= ac4hsel,
                 interpolate=True, color='royalblue')
plt.plot(t, xsel, color='k', lw=0.5, marker='o', markersize=3)
plt.plot(t, ac4hsel, color='grey', lw=0.8)
plt.plot(t, p90, color='r', lw=1.2, ls='--', label='90-percentile')
plt.xlim([0, 30])
plt.xticks([0, 7, 15, 23, 30], ['2017-01-11',
                                '2017-01-18',
                                '2017-01-26',
                                '2017-02-03',
                                '2017-02-10'],
           rotation=20)
plt.legend()
plt.ylabel('Daily maximum temperature (ºC)')
plt.ylim([20, 42.5])
plt.scatter(15, xsel[15], color='fuchsia', s=50, marker='*', zorder=5)
plt.grid(ls='--', color='gray', lw=0.5, axis='x')
basedir = '/home/tcarrasco/result/images/png/'
filename = 'heatwave_CH_2017_01_26.png'
plt.savefig(basedir + filename, dpi=300)

data = np.zeros((31,))*np.nan
time = pd.date_range('2023-01-19', '2023-02-18', freq='1d')
y = xr.DataArray(data,
                 coords=[time],
                 dims=['time'])

for i, ts in enumerate(time):
    try:
        y[i] = x.sel(time=ts).values
    except Exception as e:
        continue

# heatwave chillan 2023-02-03
p90 = np.append(p90_ene, p90_feb)[18:(18+31)]
mindate = '01-19'
maxdate = '02-18'
xsel = y.values
ac4hsel = da_ac4h.sel(time=slice('1994-'+mindate, '1994-'+maxdate)).values
t = np.arange(xsel.size)
fig = plt.figure(figsize=(12, 4))
plt.fill_between(t, ac4hsel, xsel, where=xsel > ac4hsel,
                 interpolate=True, color='gold')
plt.fill_between(t, xsel, ac4hsel, where=xsel <= ac4hsel,
                 interpolate=True, color='royalblue')
plt.plot(t, xsel, color='k', lw=0.5, marker='o', markersize=3)
plt.plot(t, ac4hsel, color='grey', lw=0.8)
plt.plot(t, p90, color='r', lw=1.2, ls='--', label='90-percentile')
plt.xlim([0, 30])
plt.xticks([0, 7, 15, 23, 30], ['2023-01-19',
                                '2023-01-26',
                                '2023-02-03',
                                '2023-02-11',
                                '2023-02-18'],
           rotation=20)
plt.legend()
plt.ylabel('Daily maximum temperature (ºC)')
plt.ylim([25, 42.5])
plt.scatter(15, xsel[15], color='fuchsia', s=50, marker='*', zorder=5)
plt.grid(ls='--', color='gray', lw=0.5, axis='x')
basedir = '/home/tcarrasco/result/images/png/'
filename = 'heatwave_CH_2023_02_03.png'
plt.savefig(basedir + filename, dpi=300)
