import numpy as np
from scipy.optimize import fmin
from scipy.stats import norm
from scipy.stats import genextreme as gev
from scipy.stats import gumbel_r as gum

# maximum likelihood estimation -- norm


def mle_norm_2d(xarr, Tarr, init_params):

    def norm_with_trend_shift(x, T, params):
        mu0 = params[0]
        sigma0 = params[1]
        alpha = params[2]
        mu = mu0 + alpha*T
        y = norm.pdf(x, mu, sigma0)
        return y

    def maxlkh(params, *args):
        xs = args[0]
        Ts = args[1]
        f = norm_with_trend_shift
        logp = -sum([np.log(f(x, T, params)) for (x, T) in zip(xs, Ts)])
        return logp

    xopt = fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))
    return xopt


# 2 degree norm
def mle_norm_2d_2(xarr, Tarr, init_params):

    def norm_with_trend_shift(x, T, params):
        mu0 = params[0]
        sigma0 = params[1]
        alpha = params[2]
        beta = params[3]
        mu = mu0 + alpha*T + beta*(T**2)
        y = norm.pdf(x, mu, sigma0)
        return y

    def maxlkh(params, *args):
        xs = args[0]
        Ts = args[1]
        f = norm_with_trend_shift
        logp = -sum([np.log(f(x, T, params)) for (x, T) in zip(xs, Ts)])
        return logp

    xopt = fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))
    return xopt


# exp
def mle_norm_2d_exp(xarr, Tarr, init_params):

    def norm_with_trend_shift(x, T, params):
        mu0 = params[0]
        sigma0 = params[1]
        alpha = params[2]
        beta = params[3]
        mu = mu0 + alpha*np.exp(beta*T)
        y = norm.pdf(x, mu, sigma0)
        return y

    def maxlkh(params, *args):
        xs = args[0]
        Ts = args[1]
        f = norm_with_trend_shift
        logp = -sum([np.log(f(x, T, params)) for (x, T) in zip(xs, Ts)])
        return logp

    xopt = fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))
    return xopt


# maximum likelihood estimation -- gev


def mle_gev_2d(xarr, Tarr, init_params):

    def gev_with_trend_shift(x, T, params):
        mu0 = params[0]
        sigma0 = params[1]
        alpha = params[2]
        eta0 = params[3]
        mu = mu0 + alpha*T
        y = gev.pdf(x, eta0, mu, sigma0)
        return y

    def maxlkh(params, *args):
        xs = args[0]
        Ts = args[1]
        f = gev_with_trend_shift
        logp = -sum([np.log(f(x, T, params)) for (x, T) in zip(xs, Ts)])
        return logp

    xopt = fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))
    return xopt


def mle_gev_2d_varsig(xarr, Tarr, init_params):

    def gev_with_trend_shift(x, T, params):
        mu0 = params[0]
        sigma0 = params[1]
        alpha = params[2]
        beta = params[3]
        eta0 = params[4]
        mu = mu0 + alpha*T
        sigma = sigma0 + beta*T
        y = gev.pdf(x, eta0, mu, sigma)
        return y

    def maxlkh(params, *args):
        xs = args[0]
        Ts = args[1]
        f = gev_with_trend_shift
        logp = -sum([np.log(f(x, T, params)) for (x, T) in zip(xs, Ts)])
        return logp

    xopt = fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))
    return xopt


def mle_gev_2d_varsig_etasig(xarr, Tarr, init_params):

    def gev_with_trend_shift(x, T, params):
        mu0 = params[0]
        sigma0 = params[1]
        eta0 = params[2]
        alpha = params[3]
        beta = params[4]
        gamma = params[5]
        mu = mu0 + alpha*T
        sigma = sigma0 + beta*T
        eta = eta0 + gamma*T
        y = gev.pdf(x, eta, mu, sigma)
        return y

    def maxlkh(params, *args):
        xs = args[0]
        Ts = args[1]
        f = gev_with_trend_shift
        logp = -sum([np.log(f(x, T, params)) for (x, T) in zip(xs, Ts)])
        return logp

    xopt = fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))
    return xopt

# maximum likelihood estimation -- gumbel


def mle_gumbel_2d(xarr, Tarr, init_params):

    def gumbel_with_trend_shift(x, T, params):
        mu0 = params[0]
        sigma0 = params[1]
        alpha = params[2]
        mu = mu0 + alpha*T
        y = gum.pdf(x, mu, sigma0)
        return y

    def maxlkh(params, *args):
        xs = args[0]
        Ts = args[1]
        f = gumbel_with_trend_shift
        logp = -sum([np.log(f(x, T, params)) for (x, T) in zip(xs, Ts)])
        return logp

    xopt = fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))
    return xopt

# maximum likelihood estimation -- norm


def mle_norm_2d_fast(xarr, Tarr, init_params):

    def norm_with_trend_shift(x, T, mu0, sigma0, alpha):
        return norm.pdf(x, mu0 + alpha*T, sigma0)

    vfun = np.vectorize(norm_with_trend_shift)

    def maxlkh(params, *args):
        return -np.sum(np.log(vfun(*args, *params)))

    return fmin(func=maxlkh, x0=init_params, args=(xarr, Tarr))


# get return periods from arg as numpy array
def return_periods(z, method='up'):
    n = z.size
    z = np.sort(z)  # sort values
    u = np.unique(z)  # get unique values
    m = u.size
    tail = np.zeros((m,))  # create matrix for tail probability and tau
    tau = np.zeros((m,))
    # compute tail and tau
    for i in range(m):
        x = u[i]
        if method == 'down':
            tail[i] = np.sum(z <= x)/n
        else:  # up
            tail[i] = np.sum(z >= x)/n
        tau[i] = 1/tail[i]
    return u, tau
