import numpy as np
from accumarray import accumarray 


def kmg2dedg(t,nargout):
    tmp=np.max(np.amax(t[:,0:3]))
    eh0=np.block([[t[:,[1,2]]],[t[:,[2,0]]],[t[:,[0,1]]]])
    eh=np.sort(eh0,1)
    ee=eh[:,0]*(tmp+1)+eh[:,1]
    u,iee,jee=np.unique(ee,return_index=True,return_inverse=True)
    e=eh[iee]
    if np.shape(t)[1]>3:
         
        eq=np.block([t[:,3],t[:,4],t[:,5]])
        e=np.block([e,eq[iee].reshape(-1,1)])
    if nargout==1:
        return e
    ne = np.size(e,0)
    he = accumarray(jee,ne)
    ib=np.argwhere(he==1)
    if nargout==2:
        return e,ib
    je=jee[...,None]
    return e,ib,je #ib,je(python)=ib,je(matlab)+1 


'''
t=np.array([[1, 2, 3],[5, 6, 7],[5, 6, 7]])
e,ib,je=kmg2dedg(t,3)
print("e=",e)
print("\n",ib)
print("\n",je)
'''