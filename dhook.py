from math import sqrt
import numpy as np

def dhook(p,*args):
    
    if (len(p.shape) == 1):
        x = p[0]
        y = p[1]
    else: 
        x=np.ravel(p[:,0])                       
        y=np.ravel(p[:,1])
        
    d1,d2,fd=[],[],[]
    if (len(p.shape) == 1):
        d1.append(sqrt(x*x+y*y)-1)
        d2.append(sqrt((x+0.4)**2+y**2)-0.55)
        fd.append(max(d1[0],-d2[0],-y))
    else : 
        for i in range(0,len(p[:,0])):
            d1.append(sqrt(x[i]*x[i]+y[i]*y[i])-1)
            d2.append(sqrt((x[i]+0.4)**2+y[i]**2)-0.55)
            fd.append(max(d1[i],-d2[i],-y[i]))
    
    return (np.array(fd))


'''
#exemple

p=np.array([1,2])
h =dhook(p)
print(h)
'''