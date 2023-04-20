import sys

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402

# use all data

tglobal, tlocal = metrics.obs_data_tmax_1d()
init_params = [37, 4, 2, 0.1]

df = metrics.gev_best_estimate(tglobal, tlocal, init_params)

basedir = "/home/tcarrasco/result/data/best_estimate/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_gev_evaluation.csv'
filepath = basedir + filename
df.to_csv(filepath)

# remove 2017

tglobal, tlocal = metrics.obs_data_tmax_1d_remove_year([2017])
init_params = [37, 4, 2, 0.1]

df = metrics.gev_best_estimate(tglobal, tlocal, init_params)

basedir = "/home/tcarrasco/result/data/best_estimate/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_gev_no2017_evaluation.csv'
filepath = basedir + filename
df.to_csv(filepath)

# remove 2023

tglobal, tlocal = metrics.obs_data_tmax_1d_remove_year([2023])
init_params = [37, 4, 2, 0.1]

df = metrics.gev_best_estimate(tglobal, tlocal, init_params)

basedir = "/home/tcarrasco/result/data/best_estimate/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_gev_no2023_evaluation.csv'
filepath = basedir + filename
df.to_csv(filepath)

# remove 2017 and 2023

tglobal, tlocal = metrics.obs_data_tmax_1d_remove_year([2017, 2023])
init_params = [36.5, 0.9, 1.2, 0.1]

df = metrics.gev_best_estimate(tglobal, tlocal, init_params)

basedir = "/home/tcarrasco/result/data/best_estimate/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_gev' +\
            '_no2017_no2023_evaluation.csv'
filepath = basedir + filename
df.to_csv(filepath)
