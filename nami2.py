# NAMI2 outline / thoughts

# this is the middle module in a series of three

# the first module does data preprocessing, creating a .csv for this module
# preprocessing can be done manually - no one should expect us
# to be able to process data from machines we have never worked with

# this modules is the most important since it contains the data processing

# the third module would do things like plotting solutes against concentration,
# plotting high affinity ligands against log concentration,
# comparing raw data in single graphs (e.g. the interactive waterfall in NAMI)

import numpy as np 
import argparse
import scipy.optimize

### argparse
# an input file - csv of three columns, first is well no., 
# second is temp., and the third is signal. First row header
# in old NAMI we had a format that we wanted to pull directly from
# but now we decide that all data should be pre-processed into
# a sensible format

tsa_data = np.genfromtxt( ... )
min_temp = tsa_data[0, 1]
max_temp = tsa_data[len(tsa_data), 1]
min_signal = np.min(tsa_data[:, 2])
max_signal = np.max(tsa_data[:, 2])

# which algorithm to use

# output graphs in .svg or .png

# average of which wells to use as reference

# shape of plate for heat map, default 8 by 12 (8 rows, 12 columns)



### NAMI classic algorithm 

# interpolate data so there are 20 data points for each degree step
# necessary to have common input whether data was sampled every 1 C
# or 0.1 C
 
cc_cutoff = 0.966 # this is a value emperically determined by the NAMI
# developer - unfortunately it should probably change depending on how
# much data was filled in by the interpolation step. If the data was sampled
# every 0.1 degrees this should probably be a bit lower and higher if 
# sampled every 1 degrees. But might not matter.

# wrap all of this in a function and repeat for each well
best_slope, best_intercept, best_cc = 0, 0, 0
best_window_size, best_window_start = 0, 0

for window_size in range(60, 401): # so an interval between 3 degrees and 20
# degrees if we interpolate to 20 data points per degree
    current_slope, current_intercept, current_cc = 0, 0, 0
    current_window_start = 0 
    for window_start in range(min_temp, max_temp-window_size):
        # calculate lin reg on tsa_data from window_start to 
        # window_start + window_size 
        if slope > current_slope:
            current_slope, current_intercept, current_cc = slope, intercept, cc
            current_window_start = window_start
    if cc > cc_cutoff:
        best_slope, best_intercept, best_cc = current_slope, current_intercept, current_cc
        best_window_size, best_window_start = window_size, current_window_start

# the melting point is calculated from the lin reg and the window_start
# plus half the window_size 

# so this goes through the data considering larger and larger windows
# in each window size it finds the steepest increase in signal
# and saves the parameters of that increase
# but only saves it as best if the correlation coefficient r is better than 
# a cut-off value. So maximizes window size but the cut-off prevents the windows 
# from becoming greater than onset and final point of protein melting.

# I'm pretty sure this could be done faster with NumPy vectorisation
# and masking but it might be fast enough as it is


## Output graphs that show parameters found for algorithm

# for each well create a graph which plots:
# the original data
# the interpolated points (smaller and more transparent)
# two vertical lines at best_window_start and best_window_start + best_window_size
# one vertical line at melting point

# algorithms should explain how they got to their result and the graph does this
# particularly important for academic software (svg will give smaller file size)




### NAMI2 alternate algorithm 

# SciPy has a function for fitting a predefined function to any data
# this may or may not need data interpolation, idk, prob not

# the function splices two 2nd order polynomials
# e.g. https://www.wolframalpha.com/input/?i=(-x%5E2%2Bx%2B30)%2F(1%2Be%5E(-1(x-0)))+%2B+(x%5E2%2Bx%2B1)%2F(1%2Be%5E(1(x-0))),+x+from+-5+to+5 
# basically fit this equation as a function of the temperature:
# signal = (s*temp**2+t*temp+u)/(1+e**(y*(temp-z))) + (v*temp**2+w*temp+x)/(1+e**(-y*(temp-z)))


# important to use good initialisation values or the fitting function won't converge
s = 0
t = 0
u = min_signal
v = 0
w = 0
x = max_signal
y = 0.1
z = (min_temp + max_temp)/2

# example of init with min_signal: 5, max_signal: 100, avg(min_max_temp): 55
# https://www.wolframalpha.com/input/?i=(0x%5E2%2B0x%2B100)%2F(1%2Be%5E(-0.1(x-55)))+%2B+(0x%5E2%2B0x%2B5)%2F(1%2Be%5E(0.1(x-55))),+x+from+-5+to+120 

# the melting temperature should be what ever the z converges on
# NOTE! this method requires a lot of testing since I have only done little

## Output graphs that show parameters found for algorithm

# for each well create a graph which plots: 
# the original data
# the fitted, extended logistic function
# the found melting point 

### Output heat map and text file 

# plot of shape given as argument with melting temperatures 
# coloured as heat map centered on the average of melting 
# temps in wells given as reference