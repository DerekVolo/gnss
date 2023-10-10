# gnss_module.py

import numpy as np
import pandas as pd
import glob
import scipy.optimize

def my_line(x, a, b):
    return a + b*x

def fit_timeseries(tlist, ylist):
    # Fit a line to the data using scipy's curve_fit
    m, mcov = scipy.optimize.curve_fit(my_line, tlist, ylist, p0=[0, 0])
    velocity = m[1]
    uncertainty = np.sqrt(mcov[1][1])
    return velocity, uncertainty

def fit_velocities(filename):
    # Load data from file
    data = np.loadtxt(filename, skiprows=1, delimiter=" ")
    t = data[:, 0]
    e, n, u = data[:, 1], data[:, 2], data[:, 3]
    
    e_vel, e_unc = fit_timeseries(t, e)
    n_vel, n_unc = fit_timeseries(t, n)
    u_vel, u_unc = fit_timeseries(t, u)
    
    return (e_vel, e_unc), (n_vel, n_unc), (u_vel, u_unc)

def get_coordinates(filename):
    data = np.loadtxt(filename)
    lat, lon, elev = data[:, 4], data[:, 5], data[:, 6]
    
    return np.mean(lat), np.mean(lon), np.mean(elev)

def fit_all_velocities(folder, pattern):
    files = glob.glob(folder + pattern)
    results = []

    for file in files:
        site_name = file.split('/')[-1].split('.')[0]
        coords = get_coordinates(file)
        e, n, u = fit_velocities(file)
        
        results.append({
            'site_name': site_name,
            'latitude': coords[0],
            'longitude': coords[1],
            'elevation': coords[2],
            'e_velocity': e[0], 'e_uncertainty': e[1],
            'n_velocity': n[0], 'n_uncertainty': n[1],
            'u_velocity': u[0], 'u_uncertainty': u[1]
        })

    return pd.DataFrame(results)
