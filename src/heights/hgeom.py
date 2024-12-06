import numpy as np


def distp(p, pp, nargout=1):
    """
    Calcule la distance entre les points de p et ceux de pp.
    """
    xp, xpp = np.meshgrid(p[:, 0], pp[:, 0])
    yp, ypp = np.meshgrid(p[:, 1], pp[:, 1])
    # Matrice des distances
    dm = np.sqrt((xp - xpp) ** 2 + (yp - ypp) ** 2)

    # Distances minimales pour chaque point de pp
    d = np.min(dm, axis=0)
    if nargout == 1:
        return d
    elif nargout == 2:
        # Indices des distances minimales
        id = np.argmin(dm, axis=0)
        return d, id
    else:
        raise ValueError("nargout doit être 1 ou 2")


def hgeom(p, fd, pmax, *args):
    """
    Fonction de taille basée sur la distance de l'axe médian.
    """
    # Constante de rapport de longueurs d'arêtes
    alpha = 0.4

    # Fonction de distance signée normalisée
    fh1 = fd(p, *args)
    fh1 = fh1 / np.max(np.abs(fh1))

    # Distance normalisée à l'axe médian
    fh2 = distp(p, pmax, 1)
    fh2 = fh2 / np.max(fh2)

    # Fonction de taille
    fh = alpha + np.abs(fh1) + fh2
    return fh
