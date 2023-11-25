# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 16:31:56 2021

@author: Jessem Ettaghouti
"""


def min_listes(l1,l2):
    lmin = []
    for i in range (len(l1)):
        lmin.append(min(l1[i],l2[i]))
    return(lmin)


def max_listes(l1,l2):
    lmax = []
    for i in range (len(l1)):
        lmax.append(max(l1[i],l2[i]))
    return(lmax)





from dcircle import dcircle
from drectangle import drectangle
import numpy as np


def dtrou(p,*args):
    r=0.25
    xc1,yc1 = -0.5,-0.5 
    xc2,yc2 = 0.5,-0.5
    xc3,yc3 = 0.5,0.5
    xc4,yc4 = -0.5,0.5
    dc1,dc2=dcircle(p,xc1,yc1,r),dcircle(p,xc2,yc2,r)
    dc3,dc4=dcircle(p,xc3,yc3,r),dcircle(p,xc4,yc4,r)
    dc = min_listes(dc1, min_listes(dc2, min_listes(dc3, dc4)))
    liste1 = drectangle(p,-1,1,-1,1)
    liste2 =  [-1 * dc[i] for i in range (len(dc))]
    fd = max_listes(liste1, liste2)
    return(np.array(fd))





'''
p = np.array([[-0.415     , -0.43      , -0.415     , -0.43      , -0.415     ],
       [-0.0387118 , -0.01273104,  0.01324972,  0.03923048,  0.06521125]]).T
print(dtrou(p))
'''
