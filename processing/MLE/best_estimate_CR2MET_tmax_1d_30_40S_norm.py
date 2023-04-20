import sys

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402

tglobal, tlocal = metrics.obs_data_tmax_1d()
init_params = [37, 4, 2]

df = metrics.norm_best_estimate(tglobal, tlocal, init_params)

basedir = "/home/tcarrasco/result/data/best_estimate/"
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_norm_evaluation.csv'
filepath = basedir + filename
df.to_csv(filepath)
