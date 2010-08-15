cdef class A:
    """
    >>> A.__init__.__doc__
    'A.__init__ docstring'
    >>> A.__len__.__doc__
    'A.__len__ docstring'
    >>> A.__add__.__doc__
    'A.__add__ docstring'
    >>> A.__getattr__.__doc__
    'A.__getattr__ docstring'
    """
    def __init__(self):
        "A.__init__ docstring"
    def __len__(self):
        "A.__len__ docstring"
    def __add__(self, other):
        "A.__add__ docstring"
    def __getattr__(self, name):
        "A.__getattr__ docstring"

cdef class B(A):
    """
    >>> B.__init__.__doc__
    'A.__init__ docstring'
    >>> B.__len__.__doc__
    'B.__len__ docstring'
    >>> B.__add__.__doc__
    'A.__add__ docstring'
    >>> B.__getattr__.__doc__
    'A.__getattr__ docstring'
    """
    def __len__(self):
        "B.__len__ docstring"

class C(A):
    """
    >>> C.__init__.__doc__
    'A.__init__ docstring'
    >>> C.__len__.__doc__
    'C.__len__ docstring'
    >>> C.__add__.__doc__
    'A.__add__ docstring'
    >>> C.__getattr__.__doc__
    'A.__getattr__ docstring'
    """
    def __len__(self):
        "C.__len__ docstring"
