import numpy as np

from distances.dcircle import dcircle
from distances.drectangle import drectangle


def dtrou(p, *args):
    """Définit la distance signée pour un carré avec quatre cercles évidés à chaque coin."""
    r = 0.25
    xc1, yc1 = -0.5, -0.5
    xc2, yc2 = 0.5, -0.5
    xc3, yc3 = 0.5, 0.5
    xc4, yc4 = -0.5, 0.5

    dc1 = dcircle(p, xc1, yc1, r)
    dc2 = dcircle(p, xc2, yc2, r)
    dc3 = dcircle(p, xc3, yc3, r)
    dc4 = dcircle(p, xc4, yc4, r)

    # Reproduction exacte de la logique MATLAB
    # min(dc1, min(dc2, min(dc3, dc4))) devient :
    dc = np.minimum(dc1, np.minimum(dc2, np.minimum(dc3, dc4)))

    # fd = max(drectangle(p,-1,1,-1,1), -dc)
    rect = drectangle(p, -1, 1, -1, 1)
    fd = np.maximum(rect, -dc)

    return fd
