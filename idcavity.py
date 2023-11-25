# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 00:47:37 2021

@author: Jessem Ettaghouti
"""

from ddcavity import ddcavity
import numpy as np

def idcavity():
    L=[]
    bbox=np.array([[-0.25,-1],[1.25,0.25]])
    pfix =  np.array([
             [-0.25,0],
             [0,0],
             [0,-1],
             [1,-1],
             [1,0],
             [1.25,0],
             [1.25,0.25],
             [-0.25,0.25]
                         ])
    L.append(ddcavity)
    L.append(bbox)
    L.append(pfix)    
    return(L)





