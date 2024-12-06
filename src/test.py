import sys

from algos.KMG2D import kmg2d
from heights.hgeom import hgeom
from heights.huniforme import huniform
from informations.idcavity import idcavity
from informations.ihook import ihook
from informations.itrou import itrou
from informations.itwocircle import itwocircle

# choix du domaine
domain = 4
# choix de la fonction de densité (1=huniform, 2=hgeom)
sizefun = 2

# Définition de fh en fonction de sizefun
if sizefun == 1:
    fh = huniform
elif sizefun == 2:
    fh = hgeom
else:
    sys.exit("Erreur: Fonction de taille inconnue.")

dg = 1
nr = 0

if domain == 1:
    fd, bbox, pfix = itrou()
    h0 = 0.03
    p, t, be, bn = kmg2d(fd, fh, h0, bbox, dg, nr, pfix)
elif domain == 2:
    fd, bbox, pfix = idcavity()
    h0 = 0.02
    p, t, be, bn = kmg2d(fd, fh, h0, bbox, dg, nr, pfix)
elif domain == 3:
    fd, bbox, pfix = ihook()
    h0 = 0.015
    p, t, be, bn = kmg2d(fd, fh, h0, bbox, dg, nr, pfix)
elif domain == 4:
    fd, bbox, pfix = itwocircle()
    h0 = 0.035
    p, t, be, bn = kmg2d(fd, fh, h0, bbox, dg, nr, pfix, 0, 0, 1, -0.4, 0, 0.5)
else:
    print("Domaine inconnu.")
    sys.exit()
