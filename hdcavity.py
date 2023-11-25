import numpy as np
def hdcavity(p,*args):
    h=[]
    for i in range(0,p.shape[0]):
        h.append(1+(7*min(p[i,1],0))**2)
    return (np.array(h))


'''
p=np.array([
    [1, 2, 3],
    [4, 5, 6]
])
hdcavity(p.T,)
'''