'''
**************************************************************************
        Projet : Génération de maillages 2D en Python
**************************************************************************
        Jessem Ettaghouti - Yassine Bahou
**************************************************************************
        ZZ2 F4 : Modélisation mathématiques et Sciences de données 
**************************************************************************
        Année Universitaire : 2021 / 2022
************************************************************************** 
'''





from itrou import itrou
from ihook import ihook 
from idcavity import idcavity 
from itwocircle import itwocircle 
from KMG2D import kmg2d
import time
import matplotlib.pyplot as plt
from edp2mur import edp2mur
import numpy as np
import sys



choix_mur = 1 # choisir si vous voulez demarrer l'algorithme du mur rectangulaire après le kmg2d

domain=4 # choix du domaine

sizefun=2 #choix de la fonction de densité


if sizefun==1:
    fhn='huniform'
elif sizefun==2:
    fhn='hgeom'
else:
    sys.exit("Erreur en hgeom")
dg=1
nr=0

if domain==1:
    fd,bbox,pfix=itrou()
    h0=0.03
    args = (fd,fhn,h0,bbox,dg,nr,pfix,())
    p,t,be,bn=kmg2d(args)
elif domain==2:
    fd,bbox,pfix=idcavity()
    h0=0.02
    args = (fd,fhn,h0,bbox,dg,nr,pfix,())
    p,t,be,bn=kmg2d(args)
elif domain==3:
    fd,bbox,pfix=ihook()
    h0=0.015
    args = (fd,fhn,h0,bbox,dg,nr,pfix,())
    p,t,be,bn=kmg2d(args)
elif domain==4:
    fd,bbox,pfix=itwocircle()
    h0=0.035
    args = (fd,fhn,h0,bbox,dg,nr,pfix,(0,0,1,-.4,0,.5))
    p,t,be,bn=kmg2d(args)
else:
    print("Domaine inconnu.")
#mesh generation
#p,t,be,bn=kmg2d(fd,fhn,h0,bbox,dg,nr,pfix,())

if choix_mur == 1:
    plt.pause(5)
    start = time.time()
    ax=1
    bx=6
    ay=1
    by=3
    nx=10
    ny=10
    p,t,bpx,bpy=edp2mur(ax,bx,ay,by,nx,ny,4)

    fig = plt.figure()
    t =t-1
    plt.triplot(np.ravel(p[:,0]), np.ravel(p[:,1]), t.copy())
    
    plt.axis('equal')
    plt.axis('off')
    fig.canvas.draw() 
    end = time.time()
    print("Temps écoulé pour le mur de triangles : ",end-start)
