# tag: pstats
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
    >>> short_stats['f_cpdef']
    200
    >>> short_stats['f_cpdef (wrapper)']
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

    >>> short_stats['withgil_prof']
    100
    >>> short_stats['withgil_noprof']
    Traceback (most recent call last):
    ...
    KeyError: 'withgil_noprof'

    >>> short_stats['nogil_prof']
    Traceback (most recent call last):
    ...
    KeyError: 'nogil_prof'
    >>> short_stats['nogil_noprof']
    Traceback (most recent call last):
    ...
    KeyError: 'nogil_noprof'

    >>> short_stats['f_raise']
    100

    >>> short_stats['m_def']
    200
    >>> short_stats['m_cdef']
    100
    >>> short_stats['m_cpdef']
    200
    >>> short_stats['m_cpdef (wrapper)']
    100

    >>> try:
    ...    os.unlink(statsfile)
    ... except:
    ...    pass

    >>> sorted(callees(s, 'test_profile'))  #doctest: +NORMALIZE_WHITESPACE
    ['f_cdef', 'f_cpdef', 'f_cpdef (wrapper)', 'f_def',
     'f_inline', 'f_inline_prof',
     'f_raise',
     'm_cdef', 'm_cpdef', 'm_cpdef (wrapper)', 'm_def',
     'withgil_prof']

    >>> profile.runctx("test_generators()", locals(), globals(), statsfile)
    >>> s = pstats.Stats(statsfile)
    >>> short_stats = dict([(k[2], v[1]) for k,v in s.stats.items()])
    >>> short_stats['generator']
    3

    >>> short_stats['generator_exception']
    2

    >>> short_stats['genexpr']
    11

    >>> sorted(callees(s, 'test_generators'))
    ['call_generator', 'call_generator_exception', 'generator_expr']

    >>> list(callees(s, 'call_generator'))
    ['generator']

    >>> list(callees(s, 'generator'))
    []

    >>> list(callees(s, 'generator_exception'))
    []

    >>> list(callees(s, 'generator_expr'))
    ['genexpr']

    >>> list(callees(s, 'genexpr'))
    []

    >>> def python_generator():
    ...   yield 1
    ...   yield 2
    >>> def call_python_generator():
    ...   list(python_generator())

    >>> profile.runctx("call_python_generator()", locals(), globals(), statsfile)
    >>> python_stats = pstats.Stats(statsfile)
    >>> python_stats_dict = dict([(k[2], v[1]) for k,v in python_stats.stats.items()])

    >>> profile.runctx("call_generator()", locals(), globals(), statsfile)
    >>> cython_stats = pstats.Stats(statsfile)
    >>> cython_stats_dict = dict([(k[2], v[1]) for k,v in cython_stats.stats.items()])

    >>> python_stats_dict['python_generator'] == cython_stats_dict['generator']
    True

    >>> try:
    ...    os.unlink(statsfile)
    ... except:
    ...    pass
"""

cimport cython

def callees(pstats, target_caller):
    pstats.calc_callees()
    for (_, _, caller), callees in pstats.all_callees.items():
      if caller == target_caller:
        for (file, line, callee) in callees.keys():
            if 'pyx' in file:
                yield callee

def test_profile(long N):
    cdef long i, n = 0
    cdef A a = A()
    for i from 0 <= i < N:
        n += f_def(i)
        n += f_cdef(i)
        n += f_cpdef(i)
        n += (<object>f_cpdef)(i)
        n += f_inline(i)
        n += f_inline_prof(i)
        n += f_noprof(i)
        n += nogil_noprof(i)
        n += nogil_prof(i)
        n += withgil_noprof(i)
        n += withgil_prof(i)
        n += a.m_def(i)
        n += (<object>a).m_def(i)
        n += a.m_cpdef(i)
        n += (<object>a).m_cpdef(i)
        n += a.m_cdef(i)
        try:
            n += f_raise(i+2)
        except RuntimeError:
            pass
    return n

def f_def(long a):
    return a

cdef long f_cdef(long a):
    return a

cpdef long f_cpdef(long a):
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

@cython.profile(False)
cdef int withgil_noprof(long a) with gil:
    return (a)
@cython.profile(True)
cdef int withgil_prof(long a) with gil:
    return (a)

@cython.profile(False)
cdef int nogil_noprof(long a) nogil:
    return a
@cython.profile(True)
cdef int nogil_prof(long a) nogil:
    return a

cdef class A(object):
    def m_def(self, long a):
        return a
    cpdef m_cpdef(self, long a):
        return a
    cdef m_cdef(self, long a):
        return a

def test_generators():
    call_generator()
    call_generator_exception()
    generator_expr()

def call_generator():
    list(generator())

def generator():
    yield 1
    yield 2

def call_generator_exception():
    try:
        list(generator_exception())
    except ValueError:
        pass

def generator_exception():
    yield 1
    raise ValueError(2)

def generator_expr():
    e = (x for x in range(10))
    return sum(e)
