import numpy as np


def tarea(p, t, nargout=1):
    """
    Calcule l'aire et la qualité des triangles.
    """
    it1, it2, it3 = t[:, 0], t[:, 1], t[:, 2]
    x21 = p[it2, 0] - p[it1, 0]
    y21 = p[it2, 1] - p[it1, 1]
    x31 = p[it3, 0] - p[it1, 0]
    y31 = p[it3, 1] - p[it1, 1]
    x32 = p[it3, 0] - p[it2, 0]
    y32 = p[it3, 1] - p[it2, 1]

    # Aire des triangles
    ar = (x21 * y31 - y21 * x31) / 2

    if nargout == 1:
        return np.abs(ar)

    # Qualité des triangles
    a1 = np.sqrt(x21**2 + y21**2)
    a2 = np.sqrt(x31**2 + y31**2)
    a3 = np.sqrt(x32**2 + y32**2)
    qt = (a2 + a3 - a1) * (a3 + a1 - a2) * (a1 + a2 - a3) / (a1 * a2 * a3)

    if nargout == 2:
        return np.abs(ar), qt

    # Longueurs des arêtes
    te = np.column_stack([a1, a2, a3])
    return np.abs(ar), qt, te
