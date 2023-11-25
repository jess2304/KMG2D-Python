import numpy as np

def huniform(p,args):
    h=[]
    for i in range(0,p.shape[0]):
        h.append(1)
    return np.array(h)

"""
p=np.array([
    [1, 2, 3],
    [4, 5, 6]
])
h =huniform(p)
"""