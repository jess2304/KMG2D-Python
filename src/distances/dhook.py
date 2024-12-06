import numpy as np


def dhook(p, *args):
    """Calcule la distance signée pour une forme de type "hook" définie par deux cercles et une condition."""
    # S'assurer que p est un tableau 2D : N x 2
    p = np.atleast_2d(p)
    x = p[:, 0]
    y = p[:, 1]

    d1 = np.sqrt(x**2 + y**2) - 1
    d2 = np.sqrt((x + 0.4) ** 2 + y**2) - 0.55

    # On crée une matrice [d1 -d2 -y] et on prend le max ligne par ligne
    fd = np.max(np.column_stack((d1, -d2, -y)), axis=1)
    return fd
