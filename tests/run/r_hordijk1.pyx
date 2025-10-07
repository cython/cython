# mode: run

cdef extern from "Python.h":
    ctypedef class __builtin__.list [object PyListObject]:
        pass


cdef class Spam(list):
    """"
    >>> try:
    ...     s = Spam()
    ... except KeyError as e:
    ...     print("Exception: %s" % e)
    ... else:
    ...     print("Did not raise the expected exception")
    Exception: 'This is not a spanish inquisition'
    """
    def __init__(self):
        raise KeyError("This is not a spanish inquisition")
