from ihook import ihook
import numpy as np



def pnodes(p,fd,h,tol,args):
    d = fd(p,args)
    iter = 0 
    pp = p
    result = []
    if d.shape[0] == 0 :
        maximum = 0
    else :
        maximum = np.max(np.abs(d))
    while (( maximum > tol ) and (iter < 10)) :
        ppx = np.array([np.ravel(pp[:,0])+h,np.ravel(pp[:,1])]).T
        
        ddx = (fd(ppx, args) - d) / h
        ppy = np.array([np.ravel(pp[:,0]),np.ravel(pp[:,1])+h]).T
        ddy = (fd(ppy, args) - d) / h
        dddx =  np.multiply(d,ddx)
        dddy = np.multiply(d,ddy)
        ddd = np.array([np.ravel(dddx),np.ravel(dddy)]).T
        pp = pp - ddd
        d = fd(pp,args)
        maximum = np.max(np.abs(d))
        iter+=1
    result.append(pp)
    result.append(iter)
    return(result)



    


'''
#on essaye
p=np.array([
    [6, 9, 2, 4, 7],
    [7, -11, 8, 4, 6]
]).T
tmp=ihook()
fd=tmp[0]
bbox=tmp[1]
ptix=tmp[2]
h0=0.015
l=pnodes(p,fd,h0,1000*h0,())
print(l)
'''