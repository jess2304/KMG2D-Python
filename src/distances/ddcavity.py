import numpy as np

from distances.drectangle import drectangle


def ddcavity(p, *args):
    """
    Définit une fonction de distance signée pour une cavité composée de deux rectangles.
    """
    d1 = drectangle(p, 0, 1, -1, 0)
    d2 = drectangle(p, -0.25, 1.25, 0, 0.25)
    # Utilisation de np.minimum pour un min élément par élément
    return np.minimum(d1, d2)
