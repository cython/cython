# mode: run

from cpython.pythread cimport *

def tss_create_delete():
    """
    >>> tss_create_delete()
    (True, False)
    """
    cdef Py_tss_t tss_key = Py_tss_NEEDS_INIT
    cdef bint after_create, after_delete
    if PyThread_tss_create(&tss_key) > 0:
        # handle key creation failure
        pass
    after_create = PyThread_tss_is_created(&tss_key) != 0
    PyThread_tss_delete(&tss_key)
    after_delete = PyThread_tss_is_created(&tss_key) != 0
    return (after_create, after_delete)

def tss_alloc_free():
    """
    >>> tss_alloc_free()
    (True, False)
    """
    cdef Py_tss_t *ptr_key
    cdef bint after_alloc, after_free
    ptr_key = PyThread_tss_alloc()
    if ptr_key == NULL:
        # handle key allocation failure
        pass
    after_alloc = PyThread_tss_is_created(ptr_key) != 0
    PyThread_tss_free(ptr_key)
    after_free = PyThread_tss_is_created(ptr_key) != 0
    return (after_alloc, after_free)

def tss_set_get():
    """
    >>> tss_set_get()
    1
    """
    cdef Py_tss_t tss_key = Py_tss_NEEDS_INIT
    cdef int the_value = 1
    cdef int ret_value
    if PyThread_tss_create(&tss_key) > 0:
        # handle key creation failure
        pass
    if PyThread_tss_get(&tss_key) == NULL:
        PyThread_tss_set(&tss_key, <void *>&the_value)
    ret_value = (<int *>PyThread_tss_get(&tss_key))[0]
    PyThread_tss_delete(&tss_key)
    return ret_value
