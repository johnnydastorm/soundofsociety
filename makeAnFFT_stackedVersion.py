# -*- coding: utf-8 -*-
"""
Created on Wed May 13 07:23:30 2020

@author: johnn
"""

# gonna try making my own continuous windowed fft thing because I should be fucking able to do this.

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fftp

sr = 44100 # sample rate in Hz
win_bins = 1024
#make a sine or saw wave for testing

f = 50 # Hz
x_samples = np.arange(sr*1.1)
sine = np.sin(2 * np.pi * f * x_samples / sr)
saw = sig.sawtooth(2*np.pi*f*x_samples / sr)
tri = sig.sawtooth(2*np.pi*f*x_samples / sr, 0.5)

#plt.plot(x_samples,saw)
#plt.plot(x_samples,sine)
#plt.scatter(sr,0)

hmg = sig.windows.hamming(win_bins,False)
#plt.plot(np.arange(hmg.size),hmg)


def jsdFFT(td,window,xover):
    # ok, first thing is amplitude window
    win_size = window.size
    half_win_size = int(win_size/xover)
    fft_size = 2 * win_size
    # go through input array in half window steps doing the window and the fft and adding to the output
    fd = np.complex128(np.zeros(shape=(len(td),fft_size)))  # a 2D array for all the FFTs
    #print(len(td),len(fd))
    portion = np.zeros(win_size)
    j=0
    for i in range (0,td.size,half_win_size):  #t.size
        print(i)
        portion *= np.zeros(win_size) #zero every time for when you get to an uneven end
        td_to_add = td[i:(i+win_size)]
        portion[:len(td_to_add)] += td_to_add
        portion *= window   #   apply the window
        full_fft = fftp.fft(portion,fft_size)  # do the fft
        fd[j,:] = full_fft      #each fft goes on a new row of a 2D array
        j+=1         
        
    return abs(fd)

def jsdIFFT(fd,window,xover):
    win_size = window.size
    half_win_size = int(win_size/xover)
    fft_size = 2 * win_size
    td = np.complex128(np.zeros(int(len(fd)/xover)))
    portion = np.zeros(fft_size)
    full_ifft = np.zeros(fft_size)
    j=0
    """ for i in range(0,8000,win_size): #len(fd)
        print(i,j)
        portion *= np.zeros(win_size)
        # run the ifft
        #plt.plot(np.arange(0,sr/2,((sr/2)/win_bins)),fd[i:i+win_size])
        portion=fftp.ifft(fd[j,i:i+win_size],win_size*2)
        portion=portion[:win_size]
        # remove the window
        #plt.plot(np.arange(len(portion)),portion)
        #plt.plot(np.arange(len(portion)),1-window)
        
        #portion /= window
        #portion = (1-window)
        #plt.plot(np.arange(len(portion)),portion)
        # stick back together
        td[j:j+win_size] += portion
        #increment half a window
        j+=1
        """
        
    for i in range (2):
        print(i)
        portion *= np.zeros(fft_size)
        portion=fftp.ifft(fd[i,:],fft_size)
        plt.plot(np.arange(portion.size),portion)
        
    return td

#plt.plot(np.arange(3*win_bins),sine[:win_bins*3])
fouriered = jsdFFT(sine,hmg,2)
dBs = 20 * np.log10(fouriered)#/max(fouriered))    
#plt.plot(np.arange(0,sr/2,(sr/(2*win_bins))),dBs[1,:win_bins])
#plt.plot (np.arange(0,sr/2,((sr/2)/win_bins)),dBs[int(10*win_bins):int(11*win_bins)])    
#plt.scatter([f,f+sr/4],[0,0],c='r')    

recovered = jsdIFFT(fouriered,hmg,2)
#plt.plot(np.arange(recovered.size),recovered)
#plt.plot(np.arange(3*win_bins),recovered[0:3*win_bins])
