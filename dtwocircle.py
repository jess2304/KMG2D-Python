from dcircle import dcircle
import numpy as np

def dtwocircle(p,args):
    xc1,yc1,rc1 = args[0],args[1],args[2]
    xc2,yc2,rc2 = args[3],args[4],args[5]
    return np.maximum(dcircle(p,xc1,yc1,rc1),-dcircle(p,xc2,yc2,rc2))

# p = np.array([[1,2,3,4,5],
#             [6,7,8,9,10]])
# print(dtwocircle(p,-0.5,-0.5,0.25,-1,-1,0.5))