import numpy as np


def huniform(p, *args):
    """
    Returne une fonction de taille de maillage uniforme avec un pas constant.
    """
    h = []
    for _ in range(0, p.shape[0]):
        h.append(1)
    return np.array(h)
