# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:35:55 2019

@author: johnn
"""
import numpy as np
import scipy.fftpack as fftp

def normaliseFractiles(d_in,bins):  # spread lower resolution data up to max resolution
    d = d_in * 1
    mx = max(d[:,0])
    d_last = d[len(d)-1,0]
    idx1 = np.where(d[:,0]==1)
    idx1 = idx1[0]
    fs = np.array(idx1)   # fractile sizes
    for i in range(1,len(fs)):
        fs[i-1] = idx1[i]-idx1[i-1]
    fs[len(fs)-1]=d_last
    
    #print(idx1,fs)
    
    fx = np.array(fs)   
    for i,x in enumerate(idx1):
        fx[i] = bins/fs[i] # fractile multiplier
        #print (fx)
        for y in range(x,x+fs[i]):
            d[y,0] = (d[y,0] * fx[i]) - (fx[i]/2)
        #print (d[:,0])
    #print(d)    
    return(d) 
    

def makeNotCumulative(d):
    o = np.array(d)
    for i in range(1,len(d)):
        o[i] = d[i]-d[i-1]
        #print (d,o)
    return(o)


#------ Audio related functions

# these two functions run ffts over an area and then run them back. I tried doing a fancy one with windows, but it was a pain and these simple ones seem to do the trick.
def noWindowFFT(td,bins):
    fft_size = bins * 2
    fd = fftp.fft(td,fft_size)
    for i in range (fft_size,td.size,fft_size):
        fd = np.append(fd,fftp.fft(td[i:i+fft_size],fft_size))
    return fd

def noWindowIFFT(fd,bins):
    fft_size = bins * 2
    td = fftp.ifft(fd,fft_size)
    for i in range (fft_size,fd.size,fft_size):
        td = np.append(td,fftp.ifft(fd[i:i+fft_size],fft_size))
    return td

def overlapFFT(td,window,overlap):
    fft_size = len(window) #* 2
    fd = fftp.fft(td[0:fft_size]*window,fft_size)
    for i in range (fft_size,td.size,int(fft_size/overlap)):
        if (len(td[i:i+fft_size]) < len(window)):
            td = np.append(td,np.zeros(len(window)-len(td[i:i+fft_size])))
        fd = np.append(fd,fftp.fft(td[i:i+fft_size]*window,fft_size))
    return fd
    
def overlapIFFT(fd,window,overlap):
    fft_size = len(window) #* 2
    win_transform = lambda x: (x / (2 * window))
    td_spread = ( (fftp.ifft(fd[0:fft_size],fft_size)) ) #win_transform
    #td_spread *= 2
    for i in range (fft_size,fd.size,fft_size):
        # convert back in bits
        td_spread = np.append(td_spread,( fftp.ifft(fd[i:i+fft_size],fft_size) ) ) # win_transform
        #then merge together 
    td_merged = np.complex128(np.zeros(int(len(td_spread)/overlap)))
    j=0
    i_jump = int(fft_size/overlap)#/overlap)
    for i in range(0,len(td_merged),i_jump):  #  18*i_jump
        #print(len(td_merged[i:i+fft_size]), len(td_spread[j:j+fft_size]))
        if (len(td_merged[i:i+fft_size]) < len(td_spread[j:j+fft_size])):
            td_merged = np.append(td_merged,np.zeros(len(td_spread[j:j+fft_size])-len(td_merged[i:i+fft_size])))
        
        td_merged[i:i+fft_size] += win_transform ( td_spread[j:j+fft_size] )#* win_transform )
        """plt.plot(np.arange(j,j+fft_size,1),td_spread[j:j+fft_size])
        plt.plot(np.arange(fft_size),td_merged[j:j+fft_size],c='black')
        plt.plot(np.arange(fft_size),win_transform,c='g')"""
        j = int(i*overlap)
    
    return td_merged

def spectralReshaper(fd,shape): # shape wants to be the same length as one set of fft bins
    #scale the shaper to the make ampl in the signal
    scaled_shape = shape * max(abs(fd))  # np.mean/np.median may also be options
    shaped_fd = np.zeros(len(fd))
    for i in range(0,len(fd),len(shape)):
        shaped_fd[i:i+len(shape)] = fd[i:i+len(shape)] * shape
    
    return shaped_fd,scaled_shape
