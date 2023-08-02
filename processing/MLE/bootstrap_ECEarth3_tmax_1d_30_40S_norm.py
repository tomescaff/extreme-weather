import sys

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402

nboot = int(sys.argv[1])
assert nboot > 0, "nboot must be a positive integer"

tglobal, tlocal = metrics.ecearth3_data_tmax_1d()
model = metrics.bootstrap_norm(tglobal, tlocal, nboot)

basedir = "/home/tcarrasco/result/data/bootstrap/"
filename = 'MLE_ECEarth3_tmax_1d_30_40S_nboot_' + str(nboot) + \
           '_norm_evaluation.nc'
filepath = basedir + filename
model.to_netcdf(filepath)
