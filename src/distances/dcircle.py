import numpy as np


def dcircle(p, *args):
    """
    Calcule la distance radiale relative d'un ensemble de points
    par rapport à un cercle défini par son centre et son rayon.
    """
    xc, yc, r = args[0], args[1], args[2]
    return np.sqrt((p[:, 0] - xc) ** 2 + (p[:, 1] - yc) ** 2) - r
