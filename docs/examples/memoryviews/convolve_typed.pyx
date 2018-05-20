import numpy as np

# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.intc

def naive_convolve(f, g):
    if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
        raise ValueError("Only odd dimensions on filter supported")
    assert f.dtype == DTYPE and g.dtype == DTYPE
    # The "cdef" keyword is also used within functions to type variables. It
    # can only be used at the top indentation level (there are non-trivial
    # problems with allowing them in other places, though we'd love to see
    # good and thought out proposals for it).

    # Py_ssize_t is the proper C type for Python array indices.
    cdef Py_ssize_t x, y, s, t, v, w, s_from, s_to, t_from, t_to

    cdef Py_ssize_t vmax = f.shape[0]
    cdef Py_ssize_t wmax = f.shape[1]
    cdef Py_ssize_t smax = g.shape[0]
    cdef Py_ssize_t tmax = g.shape[1]
    cdef Py_ssize_t smid = smax // 2
    cdef Py_ssize_t tmid = tmax // 2
    cdef Py_ssize_t xmax = vmax + 2*smid
    cdef Py_ssize_t ymax = wmax + 2*tmid
    h = np.zeros([xmax, ymax], dtype=DTYPE)
    # It is very important to type ALL your variables. You do not get any
    # warnings if not, only much slower code (they are implicitly typed as
    # Python objects).
    # For the value variable, we want to use the same data type as is
    # stored in the array, so we use int because it correspond to np.intc.
    # NB! An important side-effect of this is that if "value" overflows its
    # datatype size, it will simply wrap around like in C, rather than raise
    # an error like in Python.
    cdef int value
    for x in range(xmax):
        for y in range(ymax):
            # Cython has built-in C functions for min and max.
            # This makes the following lines very fast.
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
    return h