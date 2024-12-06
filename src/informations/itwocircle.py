import numpy as np

from distances.dtwocircle import dtwocircle


def itwocircle():
    """
    Retourne la fonction de distance `dtwocircle`,
    les coordonnées de la boîte englobante et les points fixes
    pour un domaine formé par deux cercles.
    """
    # Fonction de distance
    fd = dtwocircle
    # Boîte englobante
    bbox = np.array([[-1, -1], [1, 1]])
    # Aucun point fixe
    pfix = np.empty((0, 2))
    return fd, bbox, pfix
