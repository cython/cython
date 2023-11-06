# mode: run
# tag: warnings, numpy

cimport numpy as np
np.import_array()
# np.import_array is called - no warning necessary

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
"""
