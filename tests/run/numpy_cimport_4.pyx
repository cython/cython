# mode: run
# tag: warnings, numpy

cimport numpy
<void>numpy.import_array # dummy call should stop Cython auto-generating call to import_array

cdef extern from *:
    """
    static void** _check_array_api(void) {
        return PyArray_API; /* should be non NULL if initialized */
    }
    """
    void** _check_array_api()

def check_array_api():
    """
    >>> check_array_api()
    True
    """
    return _check_array_api() == NULL # not initialized


_WARNINGS = """
"""
