# mode: run
# tag: warnings, numpy

from numpy cimport ndarray
# np.import_array not called - should generate warning

cdef extern from *:
    """
    static void** _check_array_api(void) {
        return PyArray_API; /* should be non NULL */
    }
    """
    void** _check_array_api()

def check_array_api():
    """
    >>> check_array_api()
    True
    """
    return _check_array_api() != NULL


_WARNINGS = """
4:0: 'numpy.import_array()' has been added automatically since 'numpy' was cimported but 'numpy.import_array' was not called.
"""
