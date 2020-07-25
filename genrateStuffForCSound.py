# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:01:50 2020

@author: johnn
"""

import numpy as np
import matplotlib.pyplot as plt
import ctcsound

bins = 20
sr = 44100
f_max = sr/2

bin_freaks = np.fft.fftfreq(bins*2,(1/sr))
fcs = bin_freaks[0:bins]

plt.scatter(fcs,np.zeros(bins))

one_for_testing = fcs[2]
bw_for_testing = 90


csd = '''
<CsoundSynthesizer>
<CsOptions>
-odac -d
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
iamp = 0.7
anoise rand iamp
abp	butterbp anoise,'''+str(one_for_testing)+', '+str(bw_for_testing)+'''
	outs abp, abp
endin

</CsInstruments>
<CsScore>
i 1 0 2
</CsScore>
</CsoundSynthesizer>'''

cs = ctcsound.Csound() 

ret = cs.compileCsdText(csd)    # Compile a pre-defined .csd file
if ret == ctcsound.CSOUND_SUCCESS:
    cs.start()
    cs.perform()               
    cs.reset()
else:
    print ("didnae work")
