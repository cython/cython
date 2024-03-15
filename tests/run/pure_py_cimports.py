# mode: run
# tag: pure, import, cimport

from cython.cimports.libc import math
from cython.cimports.libc.math import ceil


def libc_math_ceil(x):
    """
    >>> libc_math_ceil(1.5)
    [2, 2]
    """
    return [int(n) for n in [ceil(x), math.ceil(x)]]


from cython.cimports.Cython.Plex import Actions
from cython.cimports.Cython.Plex.Actions import Action

def cython_package():
    """
    >>> cython_package()
    ('Action', 'Action')
    """
    return (Action.__name__, Actions.Action.__name__)
