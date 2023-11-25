# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 14:57:00 2021

@author: Jessem Ettaghouti
"""

import math as m 
import numpy as np
from  hgeom import hgeom 
from kmg2dedg import kmg2dedg
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from pnodes import pnodes 
from scipy.sparse import csr_matrix
from huniforme import huniform
import time
from kmg2dref import kmg2dref


def norme_np(evec):
    Le =[]
    for i in range (0,evec.shape[0]):
        somme =0
        for j in range(0,evec.shape[1]):
                somme += evec[i,j]**2
        Le.append(somme)
    Le = np.sqrt(np.array(Le))
    return(Le)




def recherche_point(x,p):  # retourne 1 si on ne trouve pas le point.
                           # p sera une matrice de points a deux colonnes pas a deux lignes
    i = 0 
    while((i<p.shape[0]) and ((x[0]!=p[i,0]) or (x[1]!=p[i,1])) ):
        i+=1
    if (i==p.shape[0]):
        i=1
    else :
        i=0
    return(i)




def setdiff_matrices(a,b): # matrices a deux colonnes et n lignes
#enlever les pts fixes de la mise a jour.
    
    if (a.shape[0]<b.shape[0]):
        aux=a
        a=b
        b=aux
        del aux
    n =a.shape[0]
    c= np.zeros((n,2))
    j=0
    for i in range(n):
        if (recherche_point(a[i], b) == 1): # il n'est pas là 
            c[j] = a[i]
            j+=1
    c = c[0:j]     
    del j 
    return(c)
        



def tarea(p,t, nargout):
    #calcul de l'aire et la qualité du triangle
    # p: matrice coordonnées des noeuds 
    # t: triangle vertices matrice de taille 3 ou 6
    # nombre de variables a retourner
    # si on veut avoir acces aux colonnes on considere la transposée
    it1 = t[:,0]
    it2 = t[:,1]
    it3 = t[:,2]
    
    
    
    
    x21 = np.ravel(p[it2,0]-p[it1,0])
    y21 = np.ravel(p[it2,1]-p[it1,1])
    x31 = np.ravel(p[it3,0]-p[it1,0])
    y31 = np.ravel(p[it3,1]-p[it1,1])
    x32 = np.ravel(p[it3,0]-p[it2,0])
    y32 = np.ravel(p[it3,1]-p[it2,1])
    ar = (x21 * y31 - y21 * x31 )/2
    
    a1 = np.sqrt(x21**2 + y21**2)
    a2 = np.sqrt(x31**2 + y31**2)
    a3 = np.sqrt(x32**2 + y32**2)
    qt = (a2+a3-a1)*(a3+a1-a2)*(a1+a2-a3)/(a1*a2*a3)
    
    te = np.array([a1,a2,a3])
    
    
    if (nargout ==1):
        return(ar)
    elif (nargout ==2):
        return(ar,qt)
    else:
        return(ar,qt,te)



#fd : fonction de distance ( on lui donne seulement son nom)
#fhn : le nom de la fonction de taille h(chaine de car) 
#bbox : matrice de frontieres
#dg : type de la triangulation (lineaire 1 quadratique 2)
#nr nombre de rafinements
#pfix : les noeuds fixés : matrice avec deux lignes : ligne 0 d'abscisses, ligne 1 d'ordonnées
#args[7:] : d'autres arguments (uplet)

def kmg2d(*args):
    start = time.time()
    args=args[0]
    fd,fhn,h0,bbox,dg,nr = args[0],args[1],args[2],args[3],args[4],args[5]
    #Scale factor and time step
    Fscale=1.2
    dt=0.001
    #Convergence tolerances
    eps = 2.204e-16
    epsp=0.02
    epsr=0.05 
    deps=m.sqrt(eps)*h0 
    geps=0.01*h0
    iterMax=200
    nb_fois_pnodes = 3
    mp=5
    #qualité minimale du triangle
    qmin=0.5
    
    #initialiser les points fixes
    if (len(args)>=7):
        pfix = args[6]
        npf = pfix.shape[0] #nombre de coordonnées = nombre de points
    else :
        pfix = []
        npf = 0
    arguments = args[7:][0]
    
    #---------------------------------------------------------------------------------------------------------------------------#
    
    #calcul de l'axe median approximatif
    if (fhn == "hgeom"):
        fh = hgeom
        hh0 = h0/2
        ex = np.arange(bbox[0][0],bbox[1][0],hh0)
        ey = np.arange(bbox[0][1],bbox[1][1],hh0)
        x,y= np.meshgrid(ex,ey)
        arg0 = np.array([np.ravel(x.T).tolist(),np.ravel(y.T).tolist()]).T
        
        z = fd(arg0,arguments)
        mx,nx = x.shape
        z = np.reshape(z,(mx,nx))
    
        zxy = np.gradient(z,hh0)
        zx,zy = zxy[0],zxy[1]
        
        zz = np.sqrt(zx*zx+zy*zy) 
        
        #Il faut prendre les indices des valeurs qui satisfaient les deux conditions ensemble
        imax,izzmax = [],[]
        z1 = [x for x in np.ravel(z.T)]
        zz1 = [x for x in np.ravel(zz.T)]
        for i in range(len(zz1)):
            if (zz1[i]<0.99) and (z1[i]<=0):
                izzmax.append(1)
            else :
                izzmax.append(0)
        for i in range(len(z1)):
            if izzmax[i]==1:
                imax.append(i)
        imax = np.array(imax)
        
       
        pmax = np.array([np.ravel(x.T)[imax],np.ravel(y.T)[imax]])
        pmax=pmax.T
        if (pfix.shape[0]!=0):
            pmax =np.concatenate((pmax,pfix))
       
        del ex,ey,x,y,z,zx,zy,zz,imax,zxy
    #---------------------------------------------------------------------------------------------------------------------------# 
    
    #initialiser la grille
    x,y = np.meshgrid(np.arange(bbox[0][0],bbox[1][0],h0),np.arange(bbox[0][1],bbox[1][1],h0*m.sqrt(3)/2))
    x[1:x.shape[0]+1:2] = x[1:x.shape[0]+1:2] + h0/2
    p = np.array([(x.T).flatten(),(y.T).flatten()]).T
    del x,y
    
    
    #supprimer des points en dehors de la region
    #methode de rejection
    p = p[np.where(fd(p,arguments)<geps)[0],:] 
    
    if (fhn =="hgeom"):  
        r0 = fh(p,fd,pmax,arguments)
    else:
        fh = huniform
        r0 = fh(p,arguments)
    r0 = 1/(r0**2)
    
    aux0 = pfix
    aux00 = np.random.rand(p.shape[0])<(r0/np.max(r0)) # des booleens a remettre en 0 et 1 
    aux0_0 = np.arange(aux00.shape[0])
    for i in range(aux00.shape[0]):
        aux0_0[i] = int(aux00[i])
    aux1 = p[np.where(aux0_0==1)[0],:]
    del aux00,aux0_0
    if (aux0.shape[0] != 0):
        p = np.concatenate((aux0,aux1))
    else : 
        p = aux1; 
    del aux0,aux1,r0
    #OKKK suppression terminee et taille de p (number_of_nodes,2): CA CHANGE CAR ALEATOIRE
   #----------------------------------------------------------------------------------------------#  
    # remove nodes outside the domain 
    np0 = p.shape[1]
    dp =fd(p,arguments)
    ii = np.where(dp<geps)
    ii = np.array(ii[0])
    q = p[ii,:]
    
    #Add fixed nodes : 
    if (npf>0):
      p=setdiff_matrices(q,pfix)
      p = np.concatenate((pfix,p))
    else:
        p = q
    del q,dp
    
    #------------------------------------------------------------------------------------------------#
    #initialisation de distribution
    
    plt.plot(p[:,0],p[:,1],'.')
    print('\n Initial number of nodes :',p.shape[0],'\n')
    
    
    itri = 0
    iterations = 0
    ifix = []
    tolp = 1
    tolr = 10**2
    fig=plt.figure() 
  
    plt.pause(3)
    
    #---------------------------------------------------------------------------------------------------#
    while (iterations <iterMax) and(tolp>epsp):
        iterations = iterations + 1
        
        #delaunay triangluation
        if (tolr >epsr):
            npp = p.shape[0]
            itri = 1
            p0 = p 
            t = Delaunay(p)
            plt.triplot(np.ravel(p[:,0]), np.ravel(p[:,1]), t.simplices.copy())
            
            #Reject triangles with centroid outside the domain
           
            pm = (p[t.simplices[:,0],:] + p[t.simplices[:,1],:] + p[t.simplices[:,1],:])/3
            aux1=(fd(pm,arguments)< -geps)
            aux0_0 = np.arange(aux1.shape[0])
            for i in range(aux1.shape[0]):
                    aux0_0[i] = int(aux1[i])
                    
            t.simplices = t.simplices[np.where(aux0_0==1)[0],:]
            del aux0_0,aux1
            
            
            #reorder (locally) triangle vertices counter clockwise
            
            ar = tarea(p,t.simplices,1) 
            
            it = np.where(ar<0)
            
            itt=t.simplices[it,1]
            t.simplices[it,1]=t.simplices[it,2]
            t.simplices[it,2]=itt
            #Form all edges without duplication and extract boundary nodes
            
            e,ib = kmg2dedg(t.simplices,2)
            be =e[ib,:]
            bn = np.unique(be)
            bn = bn[...,None]
            #print(bn)
            
            l = np.arange(1,npp+1)
            ii = np.setdiff1d(l,bn)
            plt.clf()
            #figure
            plt.triplot(np.ravel(p[:,0]), np.ravel(p[:,1]), t.simplices.copy())
            plt.plot(p[:,0], p[:,1],'.')
            plt.axis('equal')
            plt.axis('off')
            fig.canvas.draw()
            
            
            
            
        
        
        #Compute edge lengths and forces
        
       
        evec = p[e[:,0],:] - p[e[:,1],:]
        Le = norme_np(evec)
        
        
        if (fhn == 'hgeom'):
            
            pe = (p[e[:,0],:]+p[e[:,1],:])/2
                
            He = fh(pe,fd,pmax,arguments) 
            
            
            if len(He) == 1 :
               He = np.ravel(He)
            
        else:
            He = fh((p[e[:,0],:]+p[e[:,1],:])/2,arguments)   
        
        L0 = He * Fscale * np.sqrt(sum(Le**2)/sum(He**2))
        
        L=[]
        for i in range(0,len(Le)):
            L.append(Le[i]/L0[i])
        L=np.array(L)
        #split too long edges
        if (iterations > npp):
            il = np.where(L>1.5)[0]
            if (il.shape[0]>0):
                p = np.concatenate((p,(p[e[il,0],:]+p[e[il,1],:])/2)) 
                tolp =1
                tolr =1.2
                continue
        
        F = np.ones((1,L.shape[0]))-(L**4) * np.exp(-(L**4))
        for i in range (F.shape[1]):
            F[0,i] = F[0,i]/L[i]
    
        Fvec = np.multiply(F.T.dot(np.array([[1,1]])) , evec)
        
        print("Pourcentage : ", np.where(Fvec < 0.002)[0].shape[0] / np.ravel(Fvec).shape[0] * 100)
        
        
        
        # Assemble edge forces on nodes
        
        F = F.T
        row = np.ravel(e[:,[0,0,1,1]])
        col = np.ravel(np.ones(F.shape).dot(np.array([[0,1,0,1]])))
        #print("rows : ",row)
        data = np.ravel(np.concatenate((Fvec.T,-Fvec.T)).T)
        #print("columns : ",col)
        
        if npp < p.shape[0] : 
            npp+= (p.shape[0] - npp)
        
        Fe=csr_matrix((data,(row,col)),shape=(npp,2))
        Fe = Fe.toarray()
        
        #print("Fe : ",Fe )
        Fe[0:npf,:]=0
        
        if (iterations >npp*mp) :
            Fe[ifix,:]=0
        
        pp=p
        #--------------------------------------------------------------------------#
        #Project external nodes onto the boundary
        p = p+dt*Fe
        
        pb = p[bn[:,0],:]
        if iterations >= iterMax - nb_fois_pnodes :
            Liste_pnodes = pnodes(pb,fd,deps,1000*deps,arguments)
            p[bn[:,0],:]=Liste_pnodes[0]
            print("difference entre noeuds : ",np.max(norme_np(p-pp)))
            del Liste_pnodes                    
        
        dp = fd(p,arguments)
        
        #--------------------------------------------------------------------------#
        #Stopping criteria
        
        dp = norme_np(Fe)
        
        dp = dt*dp
        
        ii = [ii[i]-1 for i in range(len(ii))]
        
        tolp = np.max(dp[ii])/h0
        Liste=norme_np(p-p0)
        tolr =np.max(Liste) /h0
        print("tolr : ",tolr)
        del Liste
        print("La tolerance est = ",tolp)
        #Check the nodes speed if iter>mp*npp
        if (iterations > mp*npp):
            dp = norme_np(Fe)
            ifix=np.where(dp<dt*epsp)[0]
        
        
         
    #Check the triangle orientation & quality if tolp < epsp
        if (tolp < epsp):
            ar,qt,te=tarea(p,t.simplices,3)
            qtmin,itmin = np.min(qt), np.where(qt == np.min(qt))[0]
            if((np.min(ar)<0) or (qtmin < qmin)):
                tolp=1
                tolr=0.2
                ifix=np.array([])
                if (qtmin < qmin):
                    it = t.simplices[itmin,:]
                    it = np.setdiff1d(it,np.union1d(np.arange(1,npf+1),ifix)) 
                    pt = p[it,:]
                    if (it.shape[0]==3):
                        
                        ptt = (pt[0,:] +pt[1,:] +pt[2,:])/3
                        pttt = np.zeros((1,2))
                        pttt[0,0] = ptt[0]
                        pttt[0,1] = ptt[1]
                        print("taille de pttt et taille de p", pttt.shape, p.shape)
                        p = np.concatenate((p,pttt))
                    elif (it.shape[0]==2):
                        
                        ptt = (pt[0,:] +pt[1,:])/2 
                        pttt = np.zeros((1,2))
                        pttt[0,0] = ptt[0]
                        pttt[0,1] = ptt[1]
                        p=np.concatenate((p,pttt))
            if (np.min(qt)<qmin):
                print("\nLow quality triangle ",np.min(qt),"\n")
        
        print("Iteration :",iterations," | Triangulation : ",itri," | Tolerance : ",tolp," | Fixed nodes : ",len(ifix)-npf)
        itri=0
        
        
                
               
      
#checker les kmg2dref       
    if (dg > 1  or nr > 1) : 
        if (dg == 1):
            for i in range (1,nr):
                [p,t.simplices,be,bn]=kmg2dref(p,t.simplices,dg,fd,deps,1000*deps,arguments)
        else :
            for i in range(1,nr-1):
                [p,t.simplices,be,bn]=kmg2dref(p,t.simplices,1,fd,deps,1000*deps,arguments)
            [p,t.simplices,be,bn]=kmg2dref(p,t.simplices,2,fd,deps,1000*deps,arguments)
      
    plt.clf()
    print("taille finale de p et t", p.shape, t.simplices.shape)
    #plt.plot(p[:,0], p[:,1],'.')
    plt.triplot(np.ravel(p[:,0]), np.ravel(p[:,1]), t.simplices.copy())
    
    plt.axis('equal')
    plt.axis('off')
    fig.canvas.draw() 
    
    print('\nNumber of nodes ---------:',p.shape[0] ,'\n')
    print('Number of triangles--------:',t.simplices.shape[0],' \n')
    #print('Triangle quality measure---> ',np.min(qt),' \n')
    print('Number of iterations-------: ',iterations,' \n')    
    end = time.time()
    print("Temps écoulé : ",end-start)  
    

    return(p,t,be,bn)      
                           
       
# idcavity avec h0 = 0.02
# itrou avec h0 = 0.018
#ihook avec h0 = 0.15 




'''    
L = itrou()
fd = L[0]
bbox=L[1]
pfix=L[2]

fhn='hgeom'
h0=0.035
dg=1
nr=1

args = (fd,fhn,h0,bbox,dg,nr,pfix,(0,0,1,-.4,0,.5))
kmg2d(args)
'''     
        
            
            
            
            
   
    
        
      

      

 
        
        
        
        