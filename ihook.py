from dhook import dhook
import numpy as np



def ihook():
    L=[]
    bbox=np.array([
            [-1,-1],
            [1,1]])
    pfix=np.array([
            [-1,0],
            [1,0],
            [-0.95,0],
            [0.15,0]])
    L.append(dhook)
    L.append(bbox)
    L.append(pfix)
    return(L)


L=ihook()