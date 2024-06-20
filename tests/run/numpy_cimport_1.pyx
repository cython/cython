# mode: run
# tag: warnings, numpy

cimport numpy as np
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
4:8: 'numpy.import_array()' has been added automatically since 'numpy' was cimported but 'numpy.import_array' was not called.
"""
