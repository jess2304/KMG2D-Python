# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 14:03:52 2021

@author: Jessem Ettaghouti
"""

 
from dtwocircle import dtwocircle    
import numpy as np

def itwocircle():
#Retourne une liste contenant : 
    #appel a la fonction de distance 
    #reglage des frontieres
    #initialisation de pfix

    L=[]
    bbox =np.array([
            [-1,-1],
            [1,1]])
    pfix=np.array([])
    L.append(dtwocircle)
    L.append(bbox)
    L.append(pfix)
    return(L)




             