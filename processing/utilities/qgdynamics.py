import numpy as np
import xarray as xr
import scipy as sp
import scipy.ndimage
from scipy.ndimage import convolve


def smooth2(z, size):
    # Define a sizexsize box filter with all elements equal to 1
    box_filter = np.ones((size, size))
    # Normalize the filter to have a sum of 1
    box_filter /= box_filter.sum()
    # Perform convolution to apply smoothing
    smoothed_z = convolve(z, box_filter, mode='constant', cval=0.0)
    return smoothed_z


def qvector(filepath, levi=500):

    ds = xr.open_dataset(filepath)
    elat = ds['latitude'].values
    elon = ds['longitude'].values
    elev = ds['level'].values
    lon, lat = np.meshgrid(elon, elat)
    x, y = lon, lat

    z = ds['z'].sel(level=levi).squeeze().values
    u = ds['u'].sel(level=levi).squeeze().values
    v = ds['v'].sel(level=levi).squeeze().values
    T = ds['t'].sel(level=levi).squeeze().values

    z = smooth2(z, 20)
    z = z/9.8

    # some constants and f
    g = 9.8  # gravity constant
    R = 6400000  # Earth radius
    omega = 2 * np.pi / (24 * 60 * 60)
    f = 2 * omega * np.sin(np.deg2rad(y))

    # geostrophic wind
    ug = np.zeros_like(z)
    vg = np.zeros_like(z)
    ffg = np.zeros_like(z)

    dlon = 0.25*2  # known delta lon
    dlat = -0.25*2  # known delta lat

    # for i in range(1, z.shape[0] - 1):
    #     for j in range(1, z.shape[1] - 1):
    #         dx = (x[i + 1, j] - x[i - 1, j]) *
    #               (R * np.cos(np.deg2rad(y[i, j])) * np.pi / 180)
    #         dy = (y[i, j + 1] - y[i, j - 1]) * (R * np.pi / 180)

    for i in range(1, z.shape[0] - 1):
        for j in range(1, z.shape[1] - 1):
            dx = dlon * (R * np.cos(np.deg2rad(y[i, j])) * np.pi / 180)
            dy = dlat * (R * np.pi / 180)
            ug[i, j] = -g / f[i, j] * (z[i+1, j] - z[i-1, j]) / dy
            vg[i, j] = g / f[i, j] * (z[i, j+1] - z[i, j-1]) / dx

    for i in range(1, z.shape[0] - 1):
        for j in range(1, z.shape[1] - 1):
            ffg[i, j] = np.sqrt(ug[i, j]**2 + vg[i, j]**2)

    # Compute nabla T with centered finite difference
    T = smooth2(T, 30)

    gradTx = np.zeros_like(z)
    gradTy = np.zeros_like(z)
    advT = np.zeros_like(z)

    for i in range(1, z.shape[0] - 1):
        for j in range(1, z.shape[1] - 1):
            dx = dlon * (R * np.cos(np.deg2rad(y[i, j])) * np.pi / 180)
            dy = dlat * (R * np.pi / 180)
            gradTy[i, j] = (T[i+1, j] - T[i-1, j]) / dy
            gradTx[i, j] = (T[i, j+1] - T[i, j-1]) / dx
            advT[i, j] = -(u[i, j] * gradTx[i, j] + v[i, j] * gradTy[i, j])

    # Q Vector
    Q1 = np.zeros_like(z)
    Q2 = np.zeros_like(z)
    dQ = np.zeros_like(z)

    for i in range(1, z.shape[0] - 1):
        for j in range(1, z.shape[1] - 1):
            dx = dlon * (R * np.cos(np.deg2rad(y[i, j])) * np.pi / 180)
            dy = dlat * (R * np.pi / 180)
            Q1[i, j] = -((ug[i, j+1] - ug[i, j-1]) / dx * gradTx[i,
                         j] + (vg[i, j+1] - vg[i, j-1]) / dx * gradTy[i, j])
            Q2[i, j] = -((ug[i+1, j] - ug[i-1, j]) / dy * gradTx[i,
                         j] + (vg[i+1, j] - vg[i-1, j]) / dy * gradTy[i, j])

    for i in range(1, z.shape[0] - 1):
        for j in range(1, z.shape[1] - 1):
            dx = dlon * (R * np.cos(np.deg2rad(y[i, j])) * np.pi / 180)
            dy = dlat * (R * np.pi / 180)
            dQ[i, j] = (Q1[i, j+1] - Q1[i, j-1]) / dx + \
                (Q2[i+1, j] - Q2[i-1, j]) / dy

    # Scale and filter huge values
    Q1 = Q1 * 1e8
    Q2 = Q2 * 1e8
    Q1[np.abs(Q1) > 1] = 0
    Q2[np.abs(Q2) > 1] = 0

    dQ = smooth2(dQ, 30)
    dQ = dQ * 1e14

    return (Q1, Q2, dQ, elon, elat, x, y, ug, vg, u, v, z)


def geostrophic_wind(filepath):

    ds = xr.open_dataset(filepath)
    elat = ds['latitude'].values
    elon = ds['longitude'].values
    elev = ds['level'].values
    etime = ds['time']
    lon, lat = np.meshgrid(elon, elat)
    x, y = lon, lat

    z = ds['z'].values
    # z = smooth2(z, 20)
    z = z/9.8

    # some constants and f
    g = 9.8  # gravity constant
    R = 6400000  # Earth radius
    omega = 2 * np.pi / (24 * 60 * 60)
    f = 2 * omega * np.sin(np.deg2rad(y))

    # geostrophic wind
    ug = np.zeros_like(z)
    vg = np.zeros_like(z)

    dlon = 0.25*2  # known delta lon
    dlat = -0.25*2  # known delta lat

    for t in range(z.shape[0]):
        for lev in range(z.shape[1]):
            for i in range(1, z.shape[2] - 1):
                for j in range(1, z.shape[3] - 1):
                    dx = dlon * (R*np.cos(np.deg2rad(y[i, j]))*np.pi/180)
                    dy = dlat * (R * np.pi / 180)
                    ug[t, lev, i, j] = -g/f[i, j] * \
                        (z[t, lev, i+1, j] - z[t, lev, i-1, j])/dy
                    vg[t, lev, i, j] = g/f[i, j] * \
                        (z[t, lev, i, j+1] - z[t, lev, i, j-1])/dx

    coords = [etime, elev, elat, elon]
    dims = ['time', 'level', 'lat', 'lon']
    da_ug = xr.DataArray(ug, coords=coords, dims=dims)
    da_vg = xr.DataArray(vg, coords=coords, dims=dims)

    ds = xr.Dataset({'ug': da_ug, 'vg': da_vg})
    return ds
