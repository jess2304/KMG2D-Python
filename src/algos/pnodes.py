import numpy as np


def pnodes(p, fd, h, tol, *args):
    """
    Projette des points externes sur la frontière d'une région définie par une fonction de distance signée.
    """
    pp = p.copy()
    d = fd(pp, args)
    iter_count = 0

    if d.size == 0:
        maximum = 0
    else:
        maximum = np.max(np.abs(d))

    # On limite à 10 itérations
    while maximum > tol and iter_count < 10:
        ddx = (fd(np.column_stack((pp[:, 0] + h, pp[:, 1])), args) - d) / h
        ddy = (fd(np.column_stack((pp[:, 0], pp[:, 1] + h)), args) - d) / h

        # On met à jour pp sans normalisation supplémentaire
        pp[:, 0] = pp[:, 0] - d * ddx
        pp[:, 1] = pp[:, 1] - d * ddy

        d = fd(pp, args)
        maximum = np.max(np.abs(d))
        iter_count += 1

    return [pp, iter_count]
