import sys
import numpy as np

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import lens, metrics  # noqa: E402

nboot = int(sys.argv[1])
assert nboot > 0, "nboot must be a positive integer"

lens_pa = np.ravel(lens.lens1_tmax_1d_djf_30_40S_cr().values)
lens_ac = np.ravel(lens.lens1_tmax_1d_djf_30_40S_40m_present().values)
lens_fu = np.ravel(lens.lens1_tmax_1d_djf_30_40S_40m_future().values)

model = metrics.DE_bootstrap_norm(lens_pa, lens_ac, lens_fu, nboot)

basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'DE_LENS1_tmax_1d_30_40S_nboot_'+str(nboot)+'_norm_evaluation.nc'
filepath = basedir + filename
model.to_netcdf(filepath)
