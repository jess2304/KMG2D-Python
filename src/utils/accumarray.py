import numpy as np


def accumarray(indices, values=None, size=None):
    """
    Implémente accumarray de MATLAB en Python.
    """
    if values is None:
        values = np.ones_like(indices)
    if size is None:
        size = np.max(indices) + 1
    result = np.zeros(size, dtype=values.dtype)
    np.add.at(result, indices, values)
    return result
