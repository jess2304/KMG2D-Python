# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 17:21:26 2021

@author: Jessem Ettaghouti
"""



def drectangle(p,x1,x2,y1,y2):
#fonction de distance

    d=[]
    for i in range (0,p.shape[0]):
        d.append(-min((min(min(-y1+float(p[i,1]),y2-float(p[i,1])),-x1+float(p[i,0])),x2-float(p[i,0]))))
    return d

''' 
p = np.array([[-0.415     , -0.43      , -0.415     , -0.43      , -0.415     ],
       [-0.0387118 , -0.01273104,  0.01324972,  0.03923048,  0.06521125]])
'''