import pandas as pd
import xarray as xr
import sys
import matplotlib.pyplot as plt

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

# import utilities.stations as stn  # noqa: E402

import utilities.wildfires as wf  # noqa: E402

df = wf.burned_area()


# p1 = stn.tmax_1d_DJF('qn')
# p2 = stn.tmax_3d_DJF('qn')
# p3 = stn.tmax_1d_DJF('cu')
# p4 = stn.tmax_3d_DJF('cu')

# fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 7))
# p1.plot(ax=axs[0, 0], color='blue')
# p2.plot(ax=axs[1, 0], color='blue')
# p3.plot(ax=axs[0, 1], color='red')
# p4.plot(ax=axs[1, 1], color='red')

# axs[0, 0].title.set_text('Quinta Normal')
# axs[0, 1].title.set_text('General Freire')
# axs[0, 0].set_ylabel('Tmax 1d DJF (ºC)')
# axs[1, 0].set_ylabel('Tmax 3d DJF (ºC)')

# for ax in axs.ravel():
#     ax.grid(c='grey', lw=0.5, ls='--')
#     ax.set_xlabel('')

# plt.tight_layout()
# plt.savefig('/home/tcarrasco/result/images/png/tmax_stns.png', dpi=300)

# basedir = '/home/tcarrasco/result/data/CR2MET/tmax/final/'
# filename = 'CR2MET_tmax_1day_DJF_1960_2023_chile_005deg.nc'
# filepath = basedir + filename
# da = xr.open_dataset(filepath)['tmax']

# basedir = '/home/tcarrasco/result/data/CR2MET/mask/'
# filename = 'CR2MET_clmask_v2.5_mon_1960_2021_005deg.nc'
# filepath = basedir + filename
# mask = xr.open_dataset(filepath)['cl_mask']

# da = da*mask
# da = da.where((da.lat < -30.0) & (da.lat > -40.0), drop=True)
# ts = da.max(['lat', 'lon'])

# fig = plt.figure(figsize=(10, 7))
# ax = plt.gca()
# ts.plot(ax=ax, color='blue')
# ax.title.set_text('CR2MET')
# ax.set_ylabel('Tmax 1d DJF (ºC)')
# ax.grid(c='grey', lw=0.5, ls='--')
# ax.set_xlabel('')

# plt.tight_layout()
# plt.savefig('/home/tcarrasco/result/images/png/tmax_cr2.png', dpi=300)
