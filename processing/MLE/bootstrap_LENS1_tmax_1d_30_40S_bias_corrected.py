import sys

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402

nboot = int(sys.argv[1])
assert nboot > 0, "nboot must be a positive integer"

tglobal, tlocal = metrics.lens1_data_tmax_1d_1980_2023_bias_corrected()
model = metrics.bootstrap_gev(tglobal, tlocal, nboot)

basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'MLE_LENS1_tmax_1d_30_40S_nboot_'+str(nboot)+'_gev_validation.nc'
filepath = basedir + filename
model.to_netcdf(filepath)
