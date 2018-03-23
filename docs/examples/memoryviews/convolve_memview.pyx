import numpy as np

DTYPE = np.intc

# It is possible to declare types in the function declaration.
def naive_convolve(int [:,:] f, int [:,:] g):
    if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
        raise ValueError("Only odd dimensions on filter supported")

    # We don't need to check for the type of NumPy array here because
    # a check is already performed when calling the function.
    cdef Py_ssize_t x, y, s, t, v, w, s_from, s_to, t_from, t_to
    cdef Py_ssize_t vmax = f.shape[0]
    cdef Py_ssize_t wmax = f.shape[1]
    cdef Py_ssize_t smax = g.shape[0]
    cdef Py_ssize_t tmax = g.shape[1]
    cdef Py_ssize_t smid = smax // 2
    cdef Py_ssize_t tmid = tmax // 2
    cdef Py_ssize_t xmax = vmax + 2*smid
    cdef Py_ssize_t ymax = wmax + 2*tmid

    h_np =  np.zeros([xmax, ymax], dtype=DTYPE)
    cdef int [:,:] h = h_np

    cdef int value
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