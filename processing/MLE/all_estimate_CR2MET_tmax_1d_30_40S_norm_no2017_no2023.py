import sys
import pandas as pd
import xarray as xr

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402

basedir = '/home/tcarrasco/result/data/best_estimate/'
filename = 'MLE_CR2MET_tmax_1d_30_40S_best_estimate_norm_' +\
    'no2017_no2023_evaluation.csv'
filepath = basedir + filename
df = pd.read_csv(filepath, index_col=0)

# CI
nboot = 1000
basedir = '/home/tcarrasco/result/data/bootstrap/'
filename = f'MLE_CR2MET_tmax_1d_30_40S_nboot_{nboot}_norm_' +\
    'no2017_no2023_evaluation.nc'
filepath = basedir + filename
model = xr.open_dataset(filepath)

df_out = metrics.MLE_all_estimate_norm_no_eea_metrics(df, model)

basedir = "/home/tcarrasco/result/data/all_estimate/"
filename = f'MLE_CR2MET_tmax_1d_30_40S_all_estimate' +\
    f'_nboot_{nboot}_norm_no2017_no2023_evaluation.csv'
filepath = basedir + filename
df_out.to_csv(filepath)
