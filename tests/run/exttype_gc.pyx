# mode: run
# tag: gc


def create_obj(cls):
    cls()  # create and discard


cdef class BaseTypeNoGC:
    pass


cdef class ExtTypeGC(BaseTypeNoGC):
    """
    >>> create_obj(ExtTypeGC)
    >>> create_obj(ExtTypeGC)
    >>> create_obj(ExtTypeGC)

    >>> class PyExtTypeGC(ExtTypeGC): pass
    >>> create_obj(PyExtTypeGC)
    >>> create_obj(PyExtTypeGC)
    >>> create_obj(PyExtTypeGC)
    """
    cdef object attr


cdef class ExtTypeNoGC(BaseTypeNoGC):
    """
    >>> create_obj(ExtTypeNoGC)
    >>> create_obj(ExtTypeNoGC)
    >>> create_obj(ExtTypeNoGC)

    >>> class PyExtTypeNoGC(ExtTypeNoGC): pass
    >>> create_obj(PyExtTypeNoGC)
    >>> create_obj(PyExtTypeNoGC)
    >>> create_obj(PyExtTypeNoGC)
    """
    cdef int x


cdef extern from "Python.h":
    ctypedef extern class builtins.Exception[object PyBaseExceptionObject]:
        pass


cdef class Error(Exception):
    pass


cdef class GeneratedError(Error):
    """
    >>> create_obj(GeneratedError)                
    >>> create_obj(GeneratedError)                
    >>> create_obj(GeneratedError)                
                                               
    >>> class PyGeneratedError(GeneratedError): pass 
    >>> create_obj(PyGeneratedError)              
    >>> create_obj(PyGeneratedError)              
    >>> create_obj(PyGeneratedError)              
    """
    cdef object attr
