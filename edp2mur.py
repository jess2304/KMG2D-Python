import numpy as np


def edp2mur(ax,bx,ay,by,nx,ny,nargin):
    
    
    
    hx=(bx-ax)/(nx-1)
    hy=(by-ay)/(ny-1)
    tmp1=np.arange(ax,bx+hx,hx)
    tmp2=np.arange(ay,by+hy,hy)
    x,y=np.meshgrid(tmp1,tmp2)
    xx=np.transpose(x)
    yy=np.transpose(y)
    tmp1=xx.flatten('F')
    tmp2=yy.flatten('F')
    tmp1=tmp1[...,None]
    tmp2=tmp2[...,None]
    p=np.block([tmp1,tmp2])
    ip=np.arange(1,nx*ny+1)
    ib1=np.arange(1,nx+1)
    ib2=nx*(np.arange(1,ny+1))
    ib3=np.arange(nx*(ny-1)+1,nx*ny+1)
    ib4=np.arange(1,nx*ny+1,nx)
    ib23=np.union1d(ib2,ib3)
    ib34=np.union1d(ib3,ib4)
    ib14=np.union1d(ib1,ib4)
    ib12=np.union1d(ib1,ib2)
    iq1=np.setdiff1d(ip,ib23)
    iq2=np.setdiff1d(ip,ib34)
    iq3=np.setdiff1d(ip,ib14)
    iq4=np.setdiff1d(ip,ib12)
    iq1=iq1[...,None]
    iq2=iq2[...,None]
    iq3=iq3[...,None]
    iq4=iq4[...,None]
    t=np.block([[iq1,iq2,iq3],[iq3,iq4,iq1]])
    if nargin==2:
        return p,t
    bpx=np.array([ib1,ib3])
    bpy=np.array([ib4,ib2])
    return p,t,np.transpose(bpx),np.transpose(bpy)


