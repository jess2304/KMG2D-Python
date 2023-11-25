# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 00:39:23 2021

@author: Jessem Ettaghouti
"""

from dtrou import dtrou 
import numpy as np

def itrou():
    L=[]
    bbox = np.array([[-1,-1],[1,1]]) 
    pfix = np.array([[-1,-1],[1,-1],[1,1],[-1,1]])
    
    L.append(dtrou)
    L.append(bbox)
    L.append(pfix)
       
    return(L)


