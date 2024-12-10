import math as m
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.spatial import Delaunay

from algos.kmg2dedg import kmg2dedg
from algos.kmg2dref import kmg2dref
from algos.pnodes import pnodes
from utils.draw import draw
from utils.tarea import tarea


def kmg2d(
    fd,
    fh,
    h0,
    bbox,
    nr,
    pfix=None,
    canvas=None,
    root=None,
    ax=None,
    update_progress=None,
    *arguments
):
    """
    Algorithme principal de génération de maillages
    """
    # Paramètres
    Fscale = 1.2
    dt = 0.1
    epsp = 0.005
    epsr = 0.5
    deps = m.sqrt(np.finfo(float).eps) * h0
    geps = 0.001 * h0
    iterMax = 5000
    mp = 5
    qmin = 0.5
    start = time.time()
    if pfix is None:
        pfix = np.empty((0, 2))
        npf = 0
    else:
        npf = pfix.shape[0]

    # Extraire le nom de fh
    fhn = fh.__name__

    # Calcul de l'axe médian approximatif si hgeom
    if fhn.lower() == "hgeom":
        hh0 = h0 / 2
        ex = np.arange(bbox[0, 0], bbox[1, 0] + hh0, hh0)
        ey = np.arange(bbox[0, 1], bbox[1, 1] + hh0, hh0)
        X, Y = np.meshgrid(ex, ey)
        arg0 = np.column_stack((X.ravel(), Y.ravel()))
        Z = fd(arg0, *arguments).reshape(X.shape)
        zx, zy = np.gradient(Z, hh0)
        zz = np.sqrt(zx**2 + zy**2)
        mask = (zz.ravel() < 0.99) & (Z.ravel() <= 0)
        pmax = arg0[mask, :]
        if npf > 0:
            pmax = np.vstack((pmax, pfix))
    else:
        pmax = None

    # Grille initiale
    x_arr = np.arange(bbox[0, 0], bbox[1, 0] + h0, h0)
    y_arr = np.arange(bbox[0, 1], bbox[1, 1] + h0 * m.sqrt(3) / 2, h0 * m.sqrt(3) / 2)
    Xinit, Yinit = np.meshgrid(x_arr, y_arr)
    Xinit[1::2] += h0 / 2
    p = np.column_stack((Xinit.ravel(), Yinit.ravel()))

    # Suppression points hors domaine
    p = p[fd(p, *arguments) < geps, :]

    # Calcul de la fonction de taille
    if fhn.lower() == "hgeom":
        r0 = fh(p, fd, pmax, *arguments)
    else:
        r0 = fh(p, *arguments)
    r0 = 1 / (r0**2)

    # Sélection
    mask = np.random.rand(p.shape[0]) < (r0 / np.max(r0))
    p = p[mask, :]

    # Ajout pfix
    if npf > 0:
        p = np.vstack((pfix, p))

    # remove nodes outside domain
    dp = fd(p, *arguments)
    p = p[dp < geps, :]
    if npf > 0:
        # On prend les points de p qui ne sont pas dans pfix
        mask = np.ones(p.shape[0], dtype=bool)
        for i in range(p.shape[0]):
            if np.any(np.all(np.isclose(p[i], pfix, atol=1e-14), axis=1)):
                mask[i] = False
        p = p[mask, :]
        p = np.vstack((pfix, p))

    print("\n Initial number of nodes : %5d \n" % p.shape[0])

    itri = 0
    iter = 0
    ifix = []
    tolp = 1
    tolr = 10**2
    # Boucle itérative pour améliorer le rendu
    while (iter < iterMax) and (tolp > epsp):
        if hasattr(root, "stop_flag") and root.stop_flag:
            print("Arrêt forcé détecté. Fin de l'exécution.")
            return
        iter += 1
        np_count = p.shape[0]

        # Triangulation Delaunay
        if tolr > epsr:
            p0 = p.copy()
            tri = Delaunay(p)
            t = tri.simplices
            pm = (p[t[:, 0], :] + p[t[:, 1], :] + p[t[:, 2], :]) / 3.0
            inside_mask = fd(pm, *arguments) < -geps
            t = t[inside_mask, :]

            # Reorientation
            ar = tarea(p, t, 1)
            neg = np.where(ar < 0)[0]
            if neg.size > 0:
                temp = t[neg, 1].copy()
                t[neg, 1] = t[neg, 2]
                t[neg, 2] = temp

            e, ib, _ = kmg2dedg(t)
            be = e[ib, :]
            bn = np.unique(be)
            ii = np.setdiff1d(np.arange(np_count), bn)

            # Mise à jour de la figure dans Tkinter
            draw(p, t, ax, canvas, root)

            # Mise à jour de la barre de progression
            progress_value = 100 * (1 - (tolp - epsp) / (1 - epsp))
            progress_value = max(0, min(100, progress_value))
            if update_progress:
                update_progress(progress_value, iter, iterMax)

        # longueurs et forces
        evec = p[e[:, 0], :] - p[e[:, 1], :]
        Le = np.sqrt(np.sum(evec**2, axis=1))
        mid_e = (p[e[:, 0], :] + p[e[:, 1], :]) / 2.0
        if fhn.lower() == "hgeom":
            He = fh(mid_e, fd, pmax, *arguments)
        else:
            He = fh(mid_e, *arguments)
        He = np.ravel(He)
        L0 = He * Fscale * np.sqrt(np.sum(Le**2) / np.sum(He**2))
        L = Le / L0

        # split edges
        if iter > np_count:
            il = np.where(L > 1.5)[0]
            if il.size > 0:
                p = np.vstack((p, (p[e[il, 0], :] + p[e[il, 1], :]) / 2))
                tolp = 1
                tolr = 1.2
                print("Number of edges split : %3d" % il.size)
                continue

        F = ((1 - L**4) * np.exp(-(L**4))) / L
        Fvec = F[:, None] * evec

        data = np.ravel(np.column_stack((Fvec, -Fvec)))
        row = np.ravel(e[:, [0, 0, 1, 1]])
        col = np.ravel(np.array([[0, 1, 0, 1]] * len(e)))
        Fe = csr_matrix((data, (row, col)), shape=(p.shape[0], 2)).toarray()

        Fe[0:npf, :] = 0
        if iter > mp * np_count:
            speed = np.sqrt(np.sum(Fe**2, axis=1))
            ifix = np.where(speed < dt * epsp)[0]
            Fe[ifix, :] = 0

        p = p + dt * Fe

        # Project external nodes
        pb = p[bn, :]
        pbn, iterb = pnodes(pb, fd, deps, 1000 * deps, *arguments)
        p[bn, :] = pbn
        dp = fd(p, *arguments)

        dp_speed = dt * np.sqrt(np.sum(Fe**2, axis=1))
        tolp = np.max(dp_speed[ii]) / h0
        tolr = np.max(np.sqrt(np.sum((p - p0) ** 2, axis=1)) / h0)

        if iter > mp * np_count:
            speed = np.sqrt(np.sum(Fe**2, axis=1))
            ifix = np.where(speed < dt * epsp)[0]

        # Vérif qualité si tolp<epsp
        if tolp < epsp:
            ar, qt, te = tarea(p, t, 3)
            qtmin = np.min(qt)
            if np.min(ar) < 0 or qtmin < qmin:
                tolp = 1
                tolr = 1.2
                ifix = []
                if qtmin < qmin:
                    itmin = np.where(qt == qtmin)[0]
                    it = t[itmin[0], :]
                    it = np.setdiff1d(it, np.union1d(np.arange(npf), ifix))
                    pt = p[it, :]
                    """
                    Supprimer les points du triangle/segment avant d'ajouter le barycentre
                    Après suppression, les indices changent. Il vaut mieux trier it
                    Pour ne pas casser l'ordre en supprimant
                    """
                    it = np.sort(it)[::-1]
                    for idx_del in it:
                        p = np.delete(p, idx_del, axis=0)
                    if len(it) == 3:
                        ptt = (pt[0, :] + pt[1, :] + pt[2, :]) / 3.0
                        p = np.vstack((p, ptt))
                    elif len(it) == 2:
                        ptt = (pt[0, :] + pt[1, :]) / 2.0
                        p = np.vstack((p, ptt))
            if np.min(qt) < qmin:
                print("Low quality triangle qt=%12.6f" % np.min(qt))

        print(
            "iteration: %4d  triangulation: %2d  tolerance: %10.6f   Fixed nodes: %4d"
            % (iter, itri, tolp, len(ifix) - npf)
        )
        itri = 0
    # Raffinement final
    if nr >= 1:
        for i in range(nr):
            p, t, be, bn = kmg2dref(p, t, fd, deps, 1000 * deps, *arguments)

    # Mise à jour de la figure dans Tkinter
    draw(p, t, ax, canvas, root)
    # Mise à jour de la barre de progression
    progress_value = 100 * (1 - (tolp - epsp) / (1 - epsp))
    progress_value = max(0, min(100, progress_value))
    if update_progress:
        update_progress(progress_value, iter, iterMax)

    # On suppose min(qt) calculé plus haut
    # Il faudrait recalculer qt pour l'afficher ici
    ar, qt, _ = tarea(p, t, 3)
    print("\nNumber of nodes ---------: %5d" % p.shape[0])
    print("Number of triangles--------: %5d" % t.shape[0])
    print("Triangle quality measure---> %5.3f" % np.min(qt))
    print("Number of iterations-------: %4d" % iter)

    end = time.time()
    print("Time elapsed:", end - start, "s")

    plt.ioff()

    e, ib, _ = kmg2dedg(t)
    be = e[ib, :]
    bn = np.unique(be)

    return p, t, be, bn
