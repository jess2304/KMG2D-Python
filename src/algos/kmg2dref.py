import numpy as np

from algos.kmg2dedg import kmg2dedg
from algos.pnodes import pnodes


def kmg2dref(p0, t0, fd, deps, tol, *arguments):
    """
    Raffine ou enrichit un maillage triangulaire en subdivisant les triangles
    ou en ajoutant des points aux milieux des arêtes.
    """
    n = p0.shape[0]
    nt = t0.shape[0]

    e, ib, je = kmg2dedg(t0, 3)
    ne = e.shape[0]

    # Ajout des milieux d'arêtes
    mid_points = (p0[e[:, 0], :] + p0[e[:, 1], :]) / 2.0
    p = np.vstack((p0, mid_points))

    ip1 = t0[:, 0].reshape((nt, 1))
    ip2 = t0[:, 1].reshape((nt, 1))
    ip3 = t0[:, 2].reshape((nt, 1))

    pm = np.arange(n, n + ne)
    lmp = pm[je]

    # mp1, mp2, mp3
    mp1 = lmp[0:nt].reshape((nt, 1))
    mp2 = lmp[nt : 2 * nt].reshape((nt, 1))
    mp3 = lmp[2 * nt : 3 * nt].reshape((nt, 1))

    t = np.zeros((4 * nt, 3), dtype=int)
    t[0:nt, :] = np.hstack([ip1, mp1, mp3])
    t[nt : 2 * nt, :] = np.hstack([mp1, ip2, mp2])
    t[2 * nt : 3 * nt, :] = np.hstack([mp2, ip3, mp3])
    t[3 * nt : 4 * nt, :] = np.hstack([mp1, mp2, mp3])

    # pb = p[n+ib,:] car ib est 0-based et les midpoints commencent à n
    pb = p[n + ib, :]
    Liste_pnodes = pnodes(pb, fd, deps, tol, *arguments)
    p[n + ib, :] = Liste_pnodes[0]
    e2, ib2 = kmg2dedg(t, 2)
    be = e2[ib2, :]
    bn = np.unique(be)

    return p, t, be, bn
