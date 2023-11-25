import numpy as np


def dcircle(p,*args): 
    xc,yc,r = args[0],args[1],args[2]
    return np.sqrt((p[:,0]-xc)**2+(p[:,1]-yc)**2)-r

# p = np.array([[1,2,3,4,5],
#             [6,7,8,9,10]])
# print(dcircle(p,-0.5,-0.5,0.25))
