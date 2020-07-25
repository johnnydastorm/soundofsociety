# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 08:47:22 2019

@author: johnn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jsdFunctions as jsdf


df = pd.read_csv('data/wyd_88_05_for_release.csv')
d = pd.DataFrame.to_numpy(df)

ciq = 'USA' # country in question

ciq_d_idx = np.where(d[:,0]==ciq)
ciq_d_idx=ciq_d_idx[0] # this line simplifies it so it's not an array in an array for no good reason
#ciq_d = np.zeros(shape=(len(ciq_d_idx),3))
year_unique, yr_idx = np.unique(d[ciq_d_idx,2], return_index = True)
ciq_d=d[ciq_d_idx,6:9]

normalised_ciq_d = jsdf.normaliseFractiles(ciq_d,100)

#uncumulated = jsdf.makeNotCumulative(normalised_ciq_d[0:10,1])
#plt.scatter(normalised_ciq_d[0:10,0],uncumulated)

for i in range(len(yr_idx)):
    if i < (len(yr_idx)-1):
        to_plot = jsdf.makeNotCumulative(normalised_ciq_d[yr_idx[i]:yr_idx[i+1],1])
        plt.scatter(normalised_ciq_d[yr_idx[i]:yr_idx[i+1],0], to_plot)
        #plt.legend(year_unique[i])
    else:
        to_plot = jsdf.makeNotCumulative(normalised_ciq_d[yr_idx[i]:len(normalised_ciq_d),1])
        plt.scatter(normalised_ciq_d[yr_idx[i]:len(normalised_ciq_d),0],to_plot)
      

plt.legend(year_unique)
plt.title(ciq)
plt.yscale("log")
plt.xscale("log")
plt.ylabel('(uncumulated) ave per capita income (local currency)')
plt.xlabel('evenly populated population fractiles')

#plt.scatter(normalised_ciq_d[0:10,0],normalised_ciq_d[0:10,1])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  OOOOOOOH MAN ..... fix this and make it not stupid using np.vsatck, that's the append I was looking for!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!







#for i, x in enumerate(ciq_d_idx):
 #   ciq_d[i]=d[x,6:9]

#foffy = np.array(d[ciq_d_idx[0],0]) #fractiles_of_folk_for_years

#foffy[:,0]=year_unique

#for i, x in enumerate(year_unique):
#    foffy[i,1] = np.where()

#foffy[0,1] = d[0:9,6]



#ciq_newYear_idx = np.where(d[ciq_d_idx[0]:d[ciq_d_idx[len(ciq_d_idx)-1]],6]==1)



#-------------------
# old shite below
#-----------------
'''
ciq_year = []
ciq_fractile = []
ciq_folkInFractile = []
ciq_income_of_fractile = []
       


for i, x in enumerate(d[:,0]):
    if (x == ciq):
       ciq_year.append(d[i,2])
       ciq_fractile.append(d[i,6])
       ciq_folkInFractile.append(d[i,8])
       ciq_income_of_fractile.append(d[i,7])
       
year_unique, idx = np.unique(ciq_year, return_index = True)




    foffy[i,1]=np.where()
    
     

#for i in range(0, len(ciq_year)):
 #   plt.plot(ciq_fractile, ciq_folkInFractile)
    
'''
    