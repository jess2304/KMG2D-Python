import numpy as np

from utils.accumarray import accumarray


def kmg2dedg(t, nargout=3):
    """
    Extrait toutes les arêtes uniques d'une triangulation et identifie les arêtes de bord.
    """
    # np correspond à max(max(t(:,1:3)))
    # Prendre le max des 3 premières colonnes
    npmax = t[:, 0:3].max()

    # Extraire toutes les arêtes
    eh0 = np.vstack((t[:, [1, 2]], t[:, [2, 0]], t[:, [0, 1]]))

    # Trier eh ligne par ligne
    eh = np.sort(eh0, axis=1)

    # Calcule ee = eh(:,1)*(np+1)+eh(:,2)
    ee = (eh[:, 0] * (npmax + 1) + eh[:, 1]).astype(np.int64)

    # Unique pour trouver les arêtes sans duplication
    _, iee, jee = np.unique(ee, return_index=True, return_inverse=True)
    e = eh[iee, :]

    # Si triangulation à 6 nœuds, ajouter le midpoint
    if t.shape[1] > 3:
        eq = np.concatenate((t[:, 3], t[:, 4], t[:, 5]))
        e = np.hstack((e, eq[iee, None]))

    if nargout == 1:
        return e

    ne = e.shape[0]
    he = accumarray(jee, np.ones_like(jee, dtype=int), size=ne)
    ib = np.where(he == 1)[0]

    if nargout == 2:
        return e, ib
    je = jee[:, None]
    return e, ib, je
