# cython: infer_types=True
import numpy as np
cimport cython

ctypedef fused my_type:
    int
    double
    long

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef naive_convolve(my_type [:,:] f, my_type [:,:] g):
    if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
        raise ValueError("Only odd dimensions on filter supported")

    vmax = f.shape[0]
    wmax = f.shape[1]
    smax = g.shape[0]
    tmax = g.shape[1]
    smid = smax // 2
    tmid = tmax // 2
    xmax = vmax + 2*smid
    ymax = wmax + 2*tmid

    if my_type is int:
        dtype = np.intc
    elif my_type is double:
        dtype = np.double
    else:
        dtype = np.long

    h_np =  np.zeros([xmax, ymax], dtype=dtype)
    cdef my_type [:,:] h = h_np

    cdef my_type value
    for x in range(xmax):
        for y in range(ymax):
            s_from = max(smid - x, -smid)
            s_to = min((xmax - x) - smid, smid + 1)
            t_from = max(tmid - y, -tmid)
            t_to = min((ymax - y) - tmid, tmid + 1)
            value = 0
            for s in range(s_from, s_to):
                for t in range(t_from, t_to):
                    v = x - smid + s
                    w = y - tmid + t
                    value += g[smid - s, tmid - t] * f[v, w]
            h[x, y] = value
    return h_np