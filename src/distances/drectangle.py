import numpy as np


def drectangle(p, x1, x2, y1, y2):
    """Calcule la distance signée d'un ensemble de points à un rectangle défini par ses limites."""
    x = p[:, 0]
    y = p[:, 1]
    # On applique les min successifs
    d = -np.minimum(np.minimum(np.minimum(-y1 + y, y2 - y), -x1 + x), x2 - x)
    return d
