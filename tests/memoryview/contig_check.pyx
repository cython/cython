# mode: run
# tag: numpy, memoryview

import numpy as np

# Cython used to forget the "is contig" helper functions when both are used.


def copy_fortran3(double[:, :, :] mat):
    """
    >>> a = np.ones((1, 1, 1), dtype=np.float64)
    >>> c = copy_fortran3(a)
    >>> bool((a == c).all())
    True
    >>> a = np.ones((4, 6, 8), dtype=np.float64, order='F')
    >>> c = copy_fortran3(a)
    >>> bool((a == c).all())
    True
    >>> a = np.ones((4, 6, 8), dtype=np.float64, order='C')
    >>> c = copy_fortran3(a)
    >>> bool((a == c).all())
    True
    """
    cdef int x, y, z

    x, y, z = np.shape(mat)

    if 1 == x == y == z:
        # C- or F- contiguous just means "contiguous".
        if mat.is_c_contig() or mat.is_f_contig():
            return mat.base
        else:
            return np.asarray(mat.copy_fortran())
    elif mat.is_f_contig():
        return mat.base
    else:
        return np.asarray(mat.copy_fortran())


def copy_fortran2(double[:, :] mat):
    """
    >>> a = np.ones((1, 1), dtype=np.float64)
    >>> c = copy_fortran2(a)
    >>> bool((a == c).all())
    True
    >>> a = np.ones((4, 6), dtype=np.float64, order='F')
    >>> c = copy_fortran2(a)
    >>> bool((a == c).all())
    True
    >>> a = np.ones((4, 6), dtype=np.float64, order='C')
    >>> c = copy_fortran2(a)
    >>> bool((a == c).all())
    True
    """
    cdef int rows, cols

    rows, cols = np.shape(mat)

    if rows == 1 or cols == 1:
        # C- or F- contiguous just means "contiguous".
        if mat.is_c_contig() or mat.is_f_contig():
            return mat.base
        else:
            return np.asarray(mat.copy_fortran())
    elif mat.is_f_contig():
        return mat.base
    else:
        return np.asarray(mat.copy_fortran())
