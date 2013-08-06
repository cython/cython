"""
Check that Cython generates a tp_clear function that actually clears object
references to NULL instead of None.

Discussed here: http://article.gmane.org/gmane.comp.python.cython.devel/14833
"""

from cpython.ref cimport PyObject, Py_TYPE

cdef class ExtensionType:
    """
    Just a type which is handled by a specific C type (instead of PyObject)
    to check that tp_clear works when the C pointer is of a type different
    from PyObject *.
    """


# Pull tp_clear for PyTypeObject as I did not find another way to access it
# from Cython code.

cdef extern from "Python.h":
    ctypedef struct PyTypeObject:
        void (*tp_clear)(object)


cdef class TpClearFixture:
    """
    An extension type that has a tp_clear method generated to test that it
    actually clears the references to NULL.

    >>> fixture = TpClearFixture()
    >>> isinstance(fixture.extension_type, ExtensionType)
    True
    >>> isinstance(fixture.any_object, str)
    True
    >>> fixture.call_tp_clear()
    >>> fixture.check_any_object_status()
    'NULL'
    >>> fixture.check_extension_type_status()
    'NULL'
    """
    
    cdef readonly object any_object
    cdef readonly ExtensionType extension_type

    def __cinit__(self):
        self.any_object = "Hello World"
        self.extension_type = ExtensionType()

    def call_tp_clear(self):
        cdef PyTypeObject *pto = Py_TYPE(self)
        pto.tp_clear(self)

    def check_any_object_status(self):
        if <void*>(self.any_object) == NULL:
            return 'NULL'
        elif self.any_object is None:
            return 'None' 
        else:
            return 'not cleared'

    def check_extension_type_status(self):
        if <void*>(self.any_object) == NULL:
            return 'NULL'
        elif self.any_object is None:
            return 'None' 
        else:
            return 'not cleared'
