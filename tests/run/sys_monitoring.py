# mode: run
# tag: monitoring, trace
# cython: language_level=3
# cython: profile=True, linetrace=True
# distutils: define_macros=CYTHON_TRACE=1 CYTHON_TRACE_NOGIL=1

from collections import defaultdict
from contextlib import contextmanager
from functools import partial
from itertools import combinations

try:
    from sys import monitoring as smon
    E = smon.events
except ImportError:
    TOOL_ID = 0
    FUNC_EVENTS = GEN_EVENTS = ()

    __doc__ = """
    >>> True
    True
    """
else:
    TOOL_ID = smon.PROFILER_ID
    FUNC_EVENTS = (E.PY_START, E.PY_RETURN)  # , E.LINE, E.RAISE)  # <- TODO: implement
    GEN_EVENTS = FUNC_EVENTS + (E.PY_RESUME, E.PY_YIELD, E.STOP_ITERATION)
    event_name = {1 << event_id: name for name, event_id in vars(E).items()}.get

    __doc__ = """
    >>> smon.use_tool_id(TOOL_ID, 'cython-test')

    >>> with monitored_events(events=()) as collected_events:
    ...     print(test_profile(0))
    0
    >>> list(collected_events.items())  # test_profile(0)
    []

    >>> with monitored_events(events=()) as collected_events:
    ...     print(test_profile(1))
    0
    >>> list(collected_events.items())  # test_profile(1)
    []

    >>> with monitored_events(events=()) as collected_events:
    ...     print(test_profile(2))
    16
    >>> list(collected_events.items())  # test_profile(2)
    []

    >>> for num_events in range(1, len(FUNC_EVENTS)+1):
    ...     for event_set in combinations(FUNC_EVENTS, num_events):
    ...         print("-------")
    ...         with monitored_events(events=event_set) as collected_events:
    ...             result = test_profile(10)
    ...         for func_name, line_counts in sorted(collected_events.items()):
    ...             print(func_name, result,
    ...                    ', '.join(f"{names([event_id])} [{sum(counts.values())}]" for event_id, counts in sorted(line_counts.items())))
    ...         assert_events(event_set, collected_events['test_profile'])  # test_profile(10)
    -------
    f_cdef 720 PY_START [10]
    f_cpdef 720 PY_START [20]
    f_def 720 PY_START [10]
    f_inline 720 PY_START [10]
    f_inline_prof 720 PY_START [10]
    f_nogil_prof 720 PY_START [10]
    f_raise 720 PY_START [10]
    f_withgil_prof 720 PY_START [10]
    m_cdef 720 PY_START [10]
    m_cpdef 720 PY_START [20]
    m_def 720 PY_START [20]
    test_profile 720 PY_START [1]
    -------
    f_cdef 720 PY_RETURN [10]
    f_cpdef 720 PY_RETURN [20]
    f_def 720 PY_RETURN [10]
    f_inline 720 PY_RETURN [10]
    f_inline_prof 720 PY_RETURN [10]
    f_nogil_prof 720 PY_RETURN [10]
    f_withgil_prof 720 PY_RETURN [10]
    m_cdef 720 PY_RETURN [10]
    m_cpdef 720 PY_RETURN [20]
    m_def 720 PY_RETURN [20]
    test_profile 720 PY_RETURN [1]
    -------
    f_cdef 720 PY_START [10], PY_RETURN [10]
    f_cpdef 720 PY_START [20], PY_RETURN [20]
    f_def 720 PY_START [10], PY_RETURN [10]
    f_inline 720 PY_START [10], PY_RETURN [10]
    f_inline_prof 720 PY_START [10], PY_RETURN [10]
    f_nogil_prof 720 PY_START [10], PY_RETURN [10]
    f_raise 720 PY_START [10]
    f_withgil_prof 720 PY_START [10], PY_RETURN [10]
    m_cdef 720 PY_START [10], PY_RETURN [10]
    m_cpdef 720 PY_START [20], PY_RETURN [20]
    m_def 720 PY_START [20], PY_RETURN [20]
    test_profile 720 PY_START [1], PY_RETURN [1]

    >>> smon.free_tool_id(TOOL_ID)
    """


import cython


def names(event_ids):
    return ', '.join([event_name(1 << event_id) for event_id in sorted(event_ids)])


def assert_events(expected_events, collected_events, loops=10):
    missing = set(expected_events).difference(collected_events)
    surplus = set(collected_events).difference(expected_events)

    if missing:
        print(f"Expected: [{names(expected_events)}], missing: [{names(missing)}]")
    if surplus:
        print(f"Expected: [{names(expected_events)}], surplus: [{names(surplus)}]")

    collected_events = {name: dict(values) for name, values in collected_events.items()}

    return
    if cython.compiled:
        if E.PY_START in collected_events:
            print("START", collected_events[E.PY_START])
        if E.PY_RETURN in collected_events:
            print("RETURN", collected_events[E.PY_RETURN])
        print(collected_events)


@contextmanager
@cython.profile(False)
@cython.linetrace(False)
def monitored_events(events=FUNC_EVENTS, function_name="test_profile"):
    event_set = E.NO_EVENTS
    for event in events:
        event_set |= event

    collected_events = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    @cython.profile(False)
    @cython.linetrace(False)
    def count_event(event, code_obj, offset, *args):
        if not (code_obj.co_name.startswith('f_') or code_obj.co_name.startswith('m_') or code_obj.co_name == function_name):
            return
        if ' (wrapper)' in code_obj.co_name:
            return  # ignore cpdef wrapper
        if not cython.compiled and 'noprof' in code_obj.co_name:
            return
        if event == E.PY_START:
            assert offset == (code_obj.co_firstlineno if cython.compiled else 0), f"{code_obj.co_name}: {offset} != {code_obj.co_firstlineno}"
        collected_events[code_obj.co_name][event][offset] += 1

    try:
        for event in events:
            smon.register_callback(TOOL_ID, event, partial(count_event, event))
        smon.set_events(TOOL_ID, event_set)
        yield collected_events
    finally:
        smon.set_events(TOOL_ID, event_set)
        for event in events:
            smon.register_callback(TOOL_ID, event, None)


####### Traced code


def test_profile(N: cython.long):
    i: cython.long
    n: cython.long = 0
    obj: object
    a: A = A()

    for i in range(N):
        n += f_def(i)
        n += f_cdef(i)
        n += f_cpdef(i)
        obj = f_cpdef
        n += obj(i)
        n += f_inline(i)
        n += f_inline_prof(i)
        n += f_noprof(i)
        n += f_nogil_noprof(i)
        n += f_nogil_prof(i)
        n += f_withgil_noprof(i)
        n += f_withgil_prof(i)
        n += a.m_def(i)
        obj = a
        n += obj.m_def(i)
        n += a.m_cpdef(i)
        n += obj.m_cpdef(i)
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
@cython.linetrace(False)
@cython.cfunc
def f_noprof(a: cython.long) -> cython.long:
    return a

@cython.exceptval(-2)
@cython.cfunc
def f_raise(_: cython.long) -> cython.long:
    raise RuntimeError

@cython.profile(False)
@cython.linetrace(False)
@cython.with_gil
@cython.cfunc
def f_withgil_noprof(a: cython.long) -> cython.long:
    return a

@cython.profile(True)
@cython.with_gil
@cython.cfunc
def f_withgil_prof(a: cython.long) -> cython.long:
    return a

@cython.profile(False)
@cython.linetrace(False)
@cython.nogil
@cython.cfunc
def f_nogil_noprof(a: cython.long) -> cython.long:
    return a

@cython.profile(True)
@cython.nogil
@cython.cfunc
def f_nogil_prof(a: cython.long) -> cython.long:
    return a


@cython.cclass
class A:
    def m_def(self, a: cython.long):
        return a

    @cython.ccall
    def m_cpdef(self, a: cython.long):
        return a

    @cython.cfunc
    def m_cdef(self, a: cython.long) -> cython.long:
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
