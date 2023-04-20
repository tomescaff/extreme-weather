import sys
from sklearn.utils import resample as bootstrap
import numpy as np
import xarray as xr
import pandas as pd

sys.path.append('/home/tcarrasco/repo/extreme-weather/processing/')

from utilities import metrics  # noqa: E402
from utilities import math as pmath  # noqa: E402


tglobal, tlocal = metrics.lens1_data_tmax_1d()

init_params = [36.8, 1.3, 0.0, 1.1, 0.1, 0.1]
xopt = pmath.mle_gev_2d_varsig_etasig(tlocal, tglobal, init_params)
# mu0, sigma0, eta0, alpha, beta, gamma

indx = ['Best estimate']
cols = ['mu0', 'sigma0', 'eta0', 'alpha', 'beta', 'gamma']
df = pd.DataFrame(data=xopt.T, index=indx, columns=cols)


basedir = "/home/tcarrasco/result/data/best_estimate/"
filename = 'MLE_LENS1_tmax_1d_30_40S_best_estimate_gev_test_allparms_var.csv'
filepath = basedir + filename
df.to_csv(filepath)
