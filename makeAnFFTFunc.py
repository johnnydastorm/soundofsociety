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

f = 70 # Hz
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
    fft_size = window.size * 2
    fd = fftp.fft(td,fft_size)
    for i in range (fft_size,td.size,fft_size):
        fd = np.append(fd,fftp.fft(td[i:i+fft_size],fft_size))
    return fd
    
def jsdIFFT(fd,window,xover):
    fft_size = window.size * 2
    td = fftp.ifft(fd,fft_size)
    for i in range (fft_size,fd.size,fft_size):
        td = np.append(td,fftp.ifft(fd[i:i+fft_size],fft_size))
    return td


def jsdFFTOld(td,window,xover):
    # ok, first thing is amplitude window
    win_size = window.size
    half_win_size = int(win_size/xover)
    # go through input array in half window steps doing the window and the fft and adding to the output
    fd = np.complex128(np.zeros(xover*(len(td)+(len(td)%win_size))))
    #print(len(td),len(fd))
    portion = np.zeros(win_size)
    j=0
    for i in range (0,td.size,win_size):#half_win_size):  
        #print(i)
        #   apply the window
        portion *= np.zeros(win_size) #zero every time for when you get to an uneven end
        td_to_add = td[i:(i+win_size)]
        portion[:len(td_to_add)] += td_to_add
        #plt.plot(np.arange(portion.size),portion)
        portion *= window
        """if(i==0):
           plt.plot(np.arange(portion.size),portion,c='g')
        if(i==512):
            plt.plot(np.arange(half_win_size,half_win_size+portion.size),portion,c='r')
        if(i==1024):
            plt.plot(np.arange(win_size,win_size+portion.size),portion,c='b')"""
        #  run the fft on the portion
        full_fft = fftp.fft(portion,win_size*2)
        #f_to_add = fd[i:i+win_size]
        if (len(fd[i:i+win_size])<win_size):
            fd=np.pad(fd,(0,(win_size%len(fd[i:i+win_size]))),'constant', constant_values=(0))
        fd[j:j+win_size] += full_fft[0:win_size*2]
        j+=half_win_size         
        
    return fd

def jsdIFFTOld(fd,window,xover):
    win_size = window.size
    half_win_size = int(win_size/xover)
    td = np.complex128(np.zeros(int(len(fd)/xover)))
    portion = np.zeros(win_size)
    j=0
    for i in range(0,len(fd),win_size*2): #len(fd)
        print(i,j)
        portion *= np.zeros(win_size)
        # run the ifft
        #plt.plot(np.arange(0,sr/2,((sr/2)/win_bins)),fd[i:i+win_size])
        portion=fftp.ifft(fd[i:i+win_size],win_size*2)
        #plt.plot(np.arange(i,i+len(portion)),portion,c='r')
        portion=portion[:win_size]
        #plt.plot(np.arange(i,i+len(portion)),portion,c='g')
        # remove the window
        #plt.plot(np.arange(len(portion)),portion)
        #plt.plot(np.arange(len(portion)),1-window)
        
        portion /= window
        #plt.plot(np.arange(i,i+len(portion)),portion,c='blue')
        #portion = (1-window)
        #plt.plot(np.arange(len(portion)),portion)
        # stick back together
        print (len(td[j:j+win_size]))
        if (len(td[j:j+win_size]) < len(portion)):
            td=np.pad(td,(0,(len(portion)%len(td[j:j+win_size]))),'constant', constant_values=(0))
        td[j:j+win_size] += portion
        #plt.plot(np.arange(i,i+len(portion)),td[j:j+win_size],c='black')
        #increment half a window
        j+=win_size
    return td

#plt.plot(np.arange(3*win_bins),sine[:win_bins*3])
fouriered = jsdFFT(tri,hmg,2)
#dBs = 20 * np.log10(fouriered/max(fouriered))    
#plt.plot (np.arange(fd.size),fd)    
#plt.plot (np.arange(0,sr/2,((sr/2)/win_bins)),dBs[int(10*win_bins):int(11*win_bins)])    
#plt.scatter([f,f+sr/4],[0,0],c='r')    

recovered = jsdIFFT(fouriered,hmg,2) #fftp.ifft(fouriered,win_bins*2) #
#plt.plot(np.arange(0,recovered.size),recovered)
#plt.plot(np.arange(recovered.size),recovered)
#plt.plot(np.arange(4*win_bins),sine[0:4*win_bins])
#plt.plot(np.arange(4*win_bins),recovered[0:4*win_bins],c='orange')

plt.plot(x_samples,tri)
plt.plot(np.arange(recovered.size),recovered,c='orange')
plt.show();
