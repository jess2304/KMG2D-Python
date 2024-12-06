import numpy as np

from distances.dtrou import dtrou


def itrou():
    """
    Retourne la fonction de distance `dtrou`,
    les coordonnées de la boîte englobante et les points fixes
    pour un domaine en forme de carré avec trous.
    """
    # Fonction de distance
    fd = dtrou
    # Boîte englobante
    bbox = np.array([[-1, -1], [1, 1]])
    # Points fixes
    pfix = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
    return fd, bbox, pfix
