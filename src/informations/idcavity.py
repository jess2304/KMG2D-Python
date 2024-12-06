import numpy as np

from distances.ddcavity import ddcavity


def idcavity():
    """
    Retourne les informations nécessaires pour générer un maillage sur une cavité 2D.
    """
    fd = ddcavity
    bbox = np.array([[-0.25, -1], [1.25, 0.25]])
    pfix = np.array(
        [
            [-0.25, 0],
            [0, 0],
            [0, -1],
            [1, -1],
            [1, 0],
            [1.25, 0],
            [1.25, 0.25],
            [-0.25, 0.25],
        ]
    )
    return fd, bbox, pfix
