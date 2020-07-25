# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:01:24 2020

@author: johnn
"""


import ctcsound

cs = ctcsound.Csound()        # Create an instance of the Csound object
ret = cs.compile_("csound","csoundTests/noise_filtering.csd")    # Compile a pre-defined .csd file
if ret == ctcsound.CSOUND_SUCCESS:
    cs.perform()               
    cs.reset()
else:
    print ("didnae work")


