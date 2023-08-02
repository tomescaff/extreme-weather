import sys

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402

nboot = int(sys.argv[1])
assert nboot > 0, "nboot must be a positive integer"

tglobal, tlocal = metrics.obs_data_tmax_1d_remove_year([2017])
init_params = [37, 4, 2]
model = metrics.bootstrap_norm(tglobal, tlocal, nboot, init_params)

basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_nboot_' + \
    str(nboot)+'_norm_no2017_evaluation.nc'
filepath = basedir + filename
model.to_netcdf(filepath)

#

tglobal, tlocal = metrics.obs_data_tmax_1d_remove_year([2023])
init_params = [37, 4, 2]
model = metrics.bootstrap_norm(tglobal, tlocal, nboot, init_params)

basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_nboot_' + \
    str(nboot)+'_norm_no2023_evaluation.nc'
filepath = basedir + filename
model.to_netcdf(filepath)

#

tglobal, tlocal = metrics.obs_data_tmax_1d_remove_year([2017, 2023])
init_params = [36.5, 0.9, 1.2]
model = metrics.bootstrap_norm(tglobal, tlocal, nboot, init_params)

basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_nboot_' + \
    str(nboot)+'_norm_no2017_no2023_evaluation.nc'
filepath = basedir + filename
model.to_netcdf(filepath)
