import numpy as np
from kmg2dedg import kmg2dedg
from scipy.sparse import csr_matrix

def kmg2dtng(t):
    nt =np.size(t,0)
    e,_,je=kmg2dedg(t,3)
    te=np.reshape(je,(nt,3),order='F')+1
    ne=np.size(e,0)
    it=np.arange(1,nt+1)-1
    tn=np.zeros((nt,3))
    
    data1=[1 for i in range(np.size(te[:,0]))]
    data2=[2 for i in range(np.size(te[:,0]))]
    data3=[3 for i in range(np.size(te[:,0]))]
    row=it
    col1=te[:,0]-1
    col2=te[:,1]-1
    col3=te[:,2]-1
    T = csr_matrix((data1,(row, col1)),shape=(nt, ne))+csr_matrix((data2,(row, col2)),shape=(nt, ne))+csr_matrix((data3,(row, col3)),shape=(nt, ne))
    
    
    for i in range(ne):
        Ti=T[:,i].toarray()
        Ti =np.ravel(Ti)
        ii=np.argwhere(Ti!=0)
        ii=np.ravel(ii)
        ni=np.size(ii)
        if ni==2:
            tn[ii[0],Ti[ii[0]]]=ii[1]
            tn[ii[1],Ti[ii[1]]]=ii[0]
    return e,te,tn
        
# t=np.array([[1, 2, 3, 4,9,10,11],[5, 6, 7, 8,12,13,14]])
# e,Ti,ii=kmg2dtng(t)
# print("e=",e)
# print("\n",Ti)
# print("\n",ii)