import sys
import numpy as np
import xarray as xr

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import lens, metrics  # noqa: E402

lens_pa = np.ravel(lens.lens1_tmax_1d_djf_30_40S_cr().values)
lens_ac = np.ravel(lens.lens1_tmax_1d_djf_30_40S_40m_present().values)
lens_fu = np.ravel(lens.lens1_tmax_1d_djf_30_40S_40m_future().values)

nboot = 1000
tau = 100

basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'DE_LENS1_tmax_1d_30_40S_nboot_{nboot}_norm_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

df_out = metrics.DE_all_estimate_norm(lens_pa, lens_ac, lens_fu,
                                      model, tau=tau)

basedir = "/home/tcarrasco/result/data/all_estimate/"
filename = f'DE_LENS1_tmax_1d_30_40S_all_estimate' +\
    f'_nboot_{nboot}_tau_{tau}_norm_evaluation.csv'
filepath = basedir + filename
df_out.to_csv(filepath)
