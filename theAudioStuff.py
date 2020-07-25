# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:46:57 2020

@author: johnn
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fftp
import jsdFunctions as jsdf
import sounddevice as sd
#from math import *

sr = 44100 # sample rate in Hz

# make a test function for the audio - a midscoop
# let's say 20 bins
#just do it in percentiles
bins = 1024   
hmg = sig.windows.hamming(bins*2,False)#define window for fft
percentile_bin_size = 100/bins

x = np.arange(0,100,percentile_bin_size)
halfway = int(bins/2)
min_of_scoop = 0.1 # base height of scoop as fraction of max
y = abs((x-x[halfway])**3) # the function of the curve
y = y + (min_of_scoop*max(y))
# normalise the whole thing between 0 and 1
y = y / max(y)
#plt.plot(x,y)
# OK, now we scale that from 0 to 22000 Hz
top_freq = 22000 # Hz
x_scale = top_freq / max(x)
x_scaled = x * x_scale
#plt.plot(x_scaled,y)

one_sec_scaled_by_sr = np.arange(0,sr/2,(sr/2)/bins)

# ok, so that would be my imput from the data, not to make a filter.
# I think maybe I should make a bandpass filter with every bin
# or can I just do an fft on the data and scale each bin? - LET'S TRY THAT FIRST
time = 0.5; # seconds
x_samples = np.arange(sr*time) # to illustrate 1 seconds' worth of samples
# make an array of noise
noise = np.random.uniform(-1,1,len(x_samples)) # one second of noise
#plt.scatter(x_samples, noise)

# tone signals for testing
f = 5 # Hz
sine = np.sin(2 * np.pi * f * x_samples / sr)
saw = sig.sawtooth(2*np.pi*f*x_samples / sr)
tri = sig.sawtooth(2*np.pi*f*x_samples / sr, 0.5)
signal = noise # select one 

#sd.play(signal,sr,blocking=True)  # PLAY SOUND WITH THIS LINE :)

#plt.plot(np.arange(0,signal.size),signal)    



# obtain frequency domain data
#sig_fd = jsdf.noWindowFFT(signal, bins)
sig_fd = jsdf.overlapFFT(signal, hmg, 2)


#impose the image on the spectral data
shaped_fd,scaled_shape = jsdf.spectralReshaper(sig_fd, y)
plt.plot(one_sec_scaled_by_sr,sig_fd[0:bins])
plt.plot(one_sec_scaled_by_sr,scaled_shape)
plt.plot(one_sec_scaled_by_sr,shaped_fd[10*bins:11*bins],c='r')

# reconstruct shaped data
#reconstructed = np.real(jsdf.noWindowIFFT(shaped_fd, bins))
reconstructed2 = np.real(jsdf.overlapIFFT(shaped_fd, hmg,2))


# reconstruct unmanipulated data
#reconstructed = np.real(jsdf.noWindowIFFT(sig_fd, bins))
#reconstructed2 = np.real(jsdf.overlapIFFT(sig_fd, hmg,2))



#plt.plot(np.arange(0,reconstructed.size),reconstructed)
#plt.plot(np.arange(0,reconstructed2.size),reconstructed2, c='black')

#sd.play(reconstructed2,sr,blocking=True)  # PLAY SOUND WITH THIS LINE :)

#This could come in handy for getting numbers if I need to do the filtering
#bin_fs = np.fft.fftfreq(bins*2,(1/sr))

### THE ALTERNATIVE IS TO USE BP FILTERS - bin_fs can give you the centre freq's of those and we can make the crossovers be the 3dB point which, with the right Q, will correspond to the bin boundaries
### but first, let's see if using csound can make this all much easier


