import sys

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402

tglobal, tlocal = metrics.ecearth3_data_tmax_1d()

init_params = [36.8, 1.3, 1.1]
df = metrics.norm_best_estimate(tglobal, tlocal, init_params)

basedir = "/home/tcarrasco/result/data/best_estimate/"
filename = 'MLE_ECEarth3_tmax_1d_30_40S_best_estimate_norm_evaluation.csv'
filepath = basedir + filename
df.to_csv(filepath)
