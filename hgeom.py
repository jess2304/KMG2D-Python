
 

import numpy as np


def distp(p,pp,nargout):
#nargout = 1 si on veut donner juste le vecteur colonne 
#nargout = 2 si on veut donner les deux vecteurs
#calculer la distance entre un point de p et pp
    [xp,xpp]=np.meshgrid(p[:,0],pp[:,0])
    [yp,ypp]=np.meshgrid(p[:,1],pp[:,1])
    dm = np.sqrt(np.multiply((xp-xpp),(xp-xpp)) +np.multiply((yp-ypp),(yp-ypp))) #dm matrice des distances
    d=np.amin(dm,axis=0)#la ligne representant les minimaux
    #pas besoin de transposer
    if (nargout ==1):
        return(np.array(d))
    elif(nargout ==2):
        i_d=np.argmin(dm,axis=0)
        #pas besoin de transposer
        return(np.array([d,i_d]))
    else :
        return(np.array([]))

        


def hgeom(p,fd,pmax,args):
    #edge lenghts ratio constant
    alpha =0.4 
    #fonction de distance normalisee
    fh1 = fd(p,args)
    fh1=fh1 / np.max(np.abs(fh1))
    #fonction d'axes medians
    fh2=distp(p,pmax,1) #array
    fh2 = fh2/np.max(fh2)   
    #fonction de taille
    fh = alpha + np.abs(fh1) + fh2
    return(fh)


'''
p=np.array([
    [6, 9, 2, 4],
    [7, -11, 8, 4]
])

p=p.T
pmax = np.array([[1,5,7,8],[-1,-2,6,4]]).T
fd = dhook
for i in range(2):
    print(hgeom(p,fd,pmax,))
    
    
'''    