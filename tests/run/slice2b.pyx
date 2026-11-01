import sys
import cython

cdef extern from *:
    ctypedef class __builtin__.list [ object PyListObject ]:
        pass

def slice_of_typed_value():

    """
    >>> slice_of_typed_value()
    [1, 2, 3]
    """
    cdef object a = []
    cdef list L = [1, 2, 3]
    a[:] = L
    return a

if sys.version_info >= (3, 12):
    # Starting with python 3.12 slice objects are hashable

    def slice_as_dict_key():
        """
        >>> slice_as_dict_key()
        Python object
        some_value
        """
        d = { slice(1, 5): "some_value" }
        print(cython.typeof(d[1:5]))
        print(d[1:5])
