# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 00:45:44 2021

@author: Jessem Ettaghouti
"""

from drectangle import drectangle
import numpy as np
def min_listes(l1,l2):
    lmin = []
    for i in range (len(l1)):
        lmin.append(min(l1[i],l2[i]))
    return(lmin)

def ddcavity(p,*args):
    
    
    d1=drectangle(p,0,1,-1,0)
    d2=drectangle(p, -0.25, 1.25, 0, 0.25)
    
    return(np.array(min_listes(d1,d2)))

