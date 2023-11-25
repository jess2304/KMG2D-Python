import numpy as np
from kmg2dedg import kmg2dedg
from dtrou import dtrou
from pnodes import pnodes
#pour la declaration de t0 meme si c'est un vecteur declarer le comme matrix [[1,2,3]] (a regler apres)

def kmg2dref(p0,t0,dg,fd,deps,tol,args):
    n=np.size(p0,0)
    nt=np.size(t0,0)
    e,ib,je=kmg2dedg(t0,3)
    ne=np.size(e,0)
    e=e-1
    p=np.concatenate((p0,(p0[e[:,0],:]+p0[e[:,1],:])/2),axis=0)
    ip1=t0[:,0].reshape((nt,1))
    ip2=t0[:,1].reshape((nt,1))
    ip3=t0[:,2].reshape((nt,1))
    pm=np.arange(n+1,n+ne+1)
    p1=p0[e[:,0],:]+1
    p1=p1/2 
    lmp=pm[je]
    je=np.reshape(je,(1,np.size(je)))
    mp1=lmp[0:nt]
    mp2=lmp[nt:2*nt]
    mp3=lmp[2*nt:3*nt]
    
    if dg==1:
        t=np.zeros((4*nt,3))
        
        t[0:nt,:]=np.block([ip1,mp1,mp3])
        t[nt:2*nt,:]=np.block([mp1,ip2,mp2])
        t[2*nt:3*nt,:]=np.block([mp2,ip3,mp3])
        t[3*nt:4*nt,:]=np.block([mp1,mp2,mp3])
        pb=p[n+ib,:][:,0,:]
        
        Liste_pnodes = pnodes(pb,fd,deps,tol,args)
        p[n+ib,:][:,0,:] = Liste_pnodes[0]
    elif dg==2:
        t=np.zeros((nt,6))
        t[:,0:3]=t0
        t[:,3:6]= np.block([mp1,mp2,mp3])
    e,ib=kmg2dedg(t,2)
    be=e[ib,:]
    bn=np.unique(be)
    return p,t,be,bn










'''
from math import sqrt
dg=1
fd = dtrou
deps = 0.03 * sqrt(2.2204* 10 **(-16))
tol=1000*deps
t0=np.array([[1,2,3],
              [2,3,1]])
p0=np.array([[3,4],
            [2,1],
            [5,6]])

p,t,be,bn= kmg2dref(p0,t0,dg,fd,deps,tol,())
print(be)
print()
print(bn)

print("p : ",p,"\nt = ",t,"\n avec be : ",be,"\n et bn ",bn)
'''
