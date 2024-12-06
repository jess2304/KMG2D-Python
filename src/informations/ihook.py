import numpy as np

from distances.dhook import dhook


def ihook():
    """
    Retourne la fonction de distance `dhook`, les coordonnées de la boîte englobante,
    et les points fixes pour un domaine en forme de crochet (hook).
    """
    # Fonction de distance
    fd = dhook
    # Boîte englobante
    bbox = np.array([[-1, 0], [1, 1]])
    # Points fixes
    pfix = np.array([[-1, 0], [0, 1], [-0.95, 0], [0.15, 0]])
    return fd, bbox, pfix
