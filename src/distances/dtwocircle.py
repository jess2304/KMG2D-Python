import numpy as np

from distances.dcircle import dcircle


def dtwocircle(p, *args):
    """
    Définit une distance signée pour deux cercles imbriqués ou adjacents.
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = args[0]
    xc1, yc1, rc1 = args[0], args[1], args[2]
    xc2, yc2, rc2 = args[3], args[4], args[5]
    return np.maximum(dcircle(p, xc1, yc1, rc1), -dcircle(p, xc2, yc2, rc2))
