# mode: run
# tag: pstats, pure3.6
# cython: profile = True
# distutils: define_macros = CYTHON_TRACE_NOGIL=1

u"""
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
    >>> short_stats['f_inline']
    100
    >>> short_stats['f_inline_prof']
    100
    >>> try:
    ...     assert short_stats['f_noprof']
    ... except KeyError:
    ...     assert COMPILED
    ... else:
    ...     assert not COMPILED

    >>> short_stats['f_raise']
    100

    >>> short_stats['withgil_prof']
    100
    >>> try:
    ...     assert short_stats['withgil_noprof']
    ... except KeyError:
    ...     assert COMPILED
    ... else:
    ...     assert not COMPILED

    >>> short_stats['nogil_prof']
    100

    >>> try:
    ...     assert short_stats['nogil_noprof']
    ... except KeyError:
    ...     assert COMPILED
    ... else:
    ...     assert not COMPILED

    >>> short_stats['m_def']
    200
    >>> short_stats['m_cdef']
    100

    >>> short_stats['m_cpdef']
    200

    >>> try:
    ...    os.unlink(statsfile)
    ... except:
    ...    pass

    >>> sorted(list(callees(s, 'test_profile')) + (
    ...        ['f_noprof', 'nogil_noprof', 'withgil_noprof'] if COMPILED else []))  #doctest: +NORMALIZE_WHITESPACE
    ['f_cdef', 'f_cpdef', 'f_def',
     'f_inline', 'f_inline_prof',
     'f_noprof',
     'f_raise',
     'm_cdef', 'm_cpdef', 'm_def',
     'nogil_noprof', 'nogil_prof',
     'withgil_noprof', 'withgil_prof']

    >>> profile.runctx("test_generators()", locals(), globals(), statsfile)
    >>> s = pstats.Stats(statsfile)
    >>> short_stats = dict([(k[2], v[1]) for k,v in s.stats.items()])
    >>> short_stats['generator']
    3

    >>> short_stats['generator_exception']
    2

    >>> sorted(callees(s, 'test_generators'))
    ['call_generator', 'call_generator_exception']

    >>> list(callees(s, 'call_generator'))
    ['generator']

    >>> list(callees(s, 'generator'))
    []

    >>> list(callees(s, 'generator_exception'))
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

    >>> python_stats_dict['python_generator'] == cython_stats_dict['generator']  \
             or  (python_stats_dict['python_generator'], cython_stats_dict['generator'])
    True

    >>> try:
    ...    os.unlink(statsfile)
    ... except:
    ...    pass
"""

import cython

COMPILED = cython.compiled

####### Debug helper
# Use like:
#   python3 -c 'import pstats_profile_test_py as pp; pp.print_event_traces()' > pytrace.log
# Then compile the module and run:
#   python3 -c 'import pstats_profile_test_py as pp; pp.print_event_traces()' > cytrace.log
# Compare the two logs.

@cython.profile(False)
@cython.linetrace(False)
def print_event_traces():
    trace_events(test_profile)
    trace_events(test_generators)


def trace_events(func=None):
    if func is None:
        func = test_profile

    last_code_obj = [None]

    @cython.profile(False)
    @cython.linetrace(False)
    def trace_function(frame, event, arg):
        try:
            code_obj = frame.f_code
            if last_code_obj[0] is not code_obj:
                last_code_obj[0] = code_obj
                print('')
            print(f"{event:20}, {code_obj.co_name}:{code_obj.co_firstlineno}, {frame.f_lineno}, {arg}")
        except Exception as exc:
            print("EXC:", exc)
            import traceback
            traceback.print_stack()

        return trace_function

    import sys
    try:
        sys.settrace(trace_function)
        sys.setprofile(trace_function)
        func(1)
    finally:
        sys.setprofile(None)
        sys.settrace(None)


####### Test code

def callees(pstats, target_caller):
    pstats.calc_callees()
    for (_, _, caller), callees in pstats.all_callees.items():
        if caller == target_caller:
            for (file, line, callee) in callees.keys():
                if 'pstats_profile_test' in file:
                    yield callee


def test_profile(N: cython.long):
    i: cython.long
    n: cython.long = 0
    a: A = A()
    for i in range(N):
        n += f_def(i)
        n += f_cdef(i)
        n += f_cpdef(i)
        n += cython.cast(object, f_cpdef)(i)
        n += f_inline(i)
        n += f_inline_prof(i)
        n += f_noprof(i)
        n += nogil_noprof(i)
        n += nogil_prof(i)
        n += withgil_noprof(i)
        n += withgil_prof(i)
        n += a.m_def(i)
        n += cython.cast(object, a).m_def(i)
        n += a.m_cpdef(i)
        n += cython.cast(object, a).m_cpdef(i)
        n += a.m_cdef(i)
        try:
            n += f_raise(i+2)
        except RuntimeError:
            pass
    return n

def f_def(a: cython.long):
    return a

@cython.cfunc
def f_cdef(a: cython.long) -> cython.long:
    return a

@cython.ccall
def f_cpdef(a: cython.long) -> cython.long:
    return a

@cython.inline
@cython.cfunc
def f_inline(a: cython.long) -> cython.long:
    return a

@cython.profile(True)
@cython.inline
@cython.cfunc
def f_inline_prof(a: cython.long) -> cython.long:
    return a

@cython.profile(False)
@cython.inline
@cython.cfunc
def f_noprof(a: cython.long) -> cython.long:
    return a

@cython.inline
@cython.exceptval(-2)
@cython.cfunc
def f_raise(a: cython.long) -> cython.long:
    raise RuntimeError

@cython.profile(False)
@cython.with_gil
@cython.cfunc
def withgil_noprof(a: cython.long) -> cython.long:
    return (a)

@cython.profile(True)
@cython.with_gil
@cython.cfunc
def withgil_prof(a: cython.long) -> cython.long:
    return (a)

@cython.profile(False)
@cython.nogil
@cython.cfunc
def nogil_noprof(a: cython.long) -> cython.long:
    return a

@cython.profile(True)
@cython.nogil
@cython.cfunc
def nogil_prof(a: cython.long) -> cython.long:
    return a


@cython.cclass
class A(object):
    def m_def(self, a: cython.long):
        return a
    @cython.ccall
    def m_cpdef(self, a: cython.long):
        return a
    @cython.cfunc
    def m_cdef(self, a: cython.long):
        return a


def test_generators(_=None):
    call_generator()
    call_generator_exception()

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

# Generator expressions are inlined in Python 3.12 and no longer show uo in profiles.
#def generator_expr():
#    e = (x for x in range(10))
#    return sum(e)
