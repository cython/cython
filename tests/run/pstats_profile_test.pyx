# cython: profile = True

__doc__ = u"""
    >>> import os, tempfile, cProfile as profile, pstats
    >>> statsfile = tempfile.mkstemp()[1]
    >>> profile.runctx("test_profile(100)", locals(), globals(), statsfile)
    >>> s = pstats.Stats(statsfile)
    >>> short_stats = dict([(k[2], v[1]) for k,v in s.stats.items()])
    >>> short_stats['f_def']
    100
    >>> short_stats['f_cdef']
    100
    >>> short_stats['f_inline']
    100
    >>> short_stats['f_inline_prof']
    100
    >>> short_stats['f_noprof']
    Traceback (most recent call last):
    ...
    KeyError: 'f_noprof'
    >>> short_stats['f_raise']
    100
    >>> try:
    ...    os.unlink(statsfile)
    ... except:
    ...    pass
"""

import sys
if sys.version_info < (2,5):
    # disable in earlier versions
    __doc__ = """
>>> # nothing to test here ...
"""

cimport cython

def test_profile(long N):
    cdef long i, n = 0
    for i from 0 <= i < N:
        n += f_def(i)
        n += f_cdef(i)
        n += f_inline(i)
        n += f_inline_prof(i)
        n += f_noprof(i)
        try:
            n += f_raise(i+2)
        except RuntimeError:
            pass
    return n

def f_def(long a):
    return a

cdef long f_cdef(long a):
    return a

cdef inline long f_inline(long a):
    return a

@cython.profile(True)
cdef inline long f_inline_prof(long a):
    return a

@cython.profile(False)
cdef int f_noprof(long a):
    return a

cdef long f_raise(long) except -2:
    raise RuntimeError
