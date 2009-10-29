__doc__ = u"""
>>> print( "%d" % Int() )
2
>>> print( "%d" % Long() )
3
>>> print( "%d" % IntLongA() )
2
>>> print( "%d" % IntLongB() )
2
>>> print( "%d" % IntLongC() )
3

"""


def getint(int i):
    """
    >>> getint( Int() )
    2
    >>> getint( Long() )
    3
    >>> getint( IntLongA() )
    2
    >>> getint( IntLongB() )
    2
    >>> getint( IntLongC() )
    3
    """
    return i

def getlong(long long i):
    """
    >>> getlong( Int() )
    2
    >>> getlong( Long() )
    3
    >>> getlong( IntLongA() )
    2
    >>> getlong( IntLongB() )
    2
    >>> getlong( IntLongC() )
    3
    """
    return <int>i


cdef class Int:
   def __int__(self):
       return 2

cdef class Long:
   def __long__(self):
       return 3

cdef class IntLongA:
   def __int__(self):
       return 2
   def __long__(self):
       return 3

cdef class IntLongB:
   def __int__(self):
       return 2
   __long__ = __int__

cdef class IntLongC:
   def __long__(self):
       return 3
   __int__ = __long__
