# mode: run
# tag: monitoring, trace
# cython: language_level=3
# cython: profile=True, linetrace=True
# distutils: define_macros = CYTHON_TRACE_NOGIL=1

import cython

import operator
from collections import defaultdict
from contextlib import contextmanager
from functools import partial

COMPILED = cython.compiled

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
    FUNC_EVENTS = (E.PY_START, E.PY_RETURN, E.RAISE)
    GEN_EVENTS = FUNC_EVENTS + (E.PY_RESUME, E.PY_YIELD)  # , E.STOP_ITERATION)
    event_name = {1 << event_id: name for name, event_id in vars(E).items()}.get

    ####### Debug helper
    # Use like:
    #   python3 -c 'import sys_monitoring as sm; sm.print_event_traces()' > pytrace.log
    # Then compile the module and run:
    #   python3 -c 'import sys_monitoring as sm; sm.print_event_traces()' > cytrace.log
    # Compare the two logs.

    ALL_EVENTS = sorted([(name, value) for (name, value) in vars(E).items() if value != 0], key=operator.itemgetter(1))

    @cython.profile(False)
    @cython.linetrace(False)
    def print_event_traces():
        trace_events(test_profile)
        trace_events(test_generators)

    @cython.profile(False)
    @cython.linetrace(False)
    def trace_events(func=None, events=ALL_EVENTS):
        event_set = E.NO_EVENTS
        for _, event in events:
            event_set |= event

        last_code_obj = [None]

        @cython.profile(False)
        @cython.linetrace(False)
        def print_event(event, code_obj, offset, *args):
            if last_code_obj[0] is not code_obj:
                last_code_obj[0] = code_obj
                print()
            print(f"{event}, {code_obj.co_name}:{code_obj.co_firstlineno}, {offset}{', ' if args else ''}", *args)

        try:
            smon.use_tool_id(TOOL_ID, 'cython-test')
            for name, event in events:
                smon.register_callback(TOOL_ID, event, partial(print_event, name))
            smon.set_events(TOOL_ID, event_set)

            result = func(1) if func is not None else test_profile(1)

        finally:
            smon.set_events(TOOL_ID, event_set)
            for _, event in events:
                smon.register_callback(TOOL_ID, event, None)
            smon.free_tool_id(TOOL_ID)

        return result

    ####### Doctests

    __doc__ = """
    >>> from itertools import combinations

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
    22
    >>> list(collected_events.items())  # test_profile(2)
    []


    ## Testing combinations of events:

    >>> for num_events in range(1, len(FUNC_EVENTS)+1):  # doctest: +REPORT_NDIFF
    ...     for event_set in combinations(FUNC_EVENTS, num_events):
    ...         print(f"--- {names(event_set)} ---")
    ...         with monitored_events(events=event_set + (E.RERAISE, E.PY_UNWIND)) as collected_events:
    ...             result = test_profile(10)
    ...         print(result)
    ...         print_events(collected_events)
    ...         assert_events(event_set, collected_events['test_profile'])  # test_profile(10)
    --- PY_START ---
    990
    f_cdef PY_START [10]
    f_cpdef PY_START [20]
    f_def PY_START [10]
    f_inline PY_START [10]
    f_inline_prof PY_START [10]
    f_nogil_prof PY_START [10]
    f_raise PY_START [20], PY_UNWIND [20]
    f_reraise PY_START [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_START [10]
    f_return_none PY_START [10]
    f_withgil_prof PY_START [10]
    m_cdef PY_START [10]
    m_classmethod PY_START [10]
    m_cpdef PY_START [20]
    m_def PY_START [20]
    m_staticmethod PY_START [10]
    test_profile PY_START [1]
    --- PY_RETURN ---
    990
    f_cdef PY_RETURN [10]
    f_cpdef PY_RETURN [20]
    f_def PY_RETURN [10]
    f_inline PY_RETURN [10]
    f_inline_prof PY_RETURN [10]
    f_nogil_prof PY_RETURN [10]
    f_raise PY_UNWIND [20]
    f_reraise PY_UNWIND [10], RERAISE [10]
    f_return_default PY_RETURN [10]
    f_return_none PY_RETURN [10]
    f_withgil_prof PY_RETURN [10]
    m_cdef PY_RETURN [10]
    m_classmethod PY_RETURN [10]
    m_cpdef PY_RETURN [20]
    m_def PY_RETURN [20]
    m_staticmethod PY_RETURN [10]
    test_profile PY_RETURN [1]
    --- RAISE ---
    990
    f_raise RAISE [20], PY_UNWIND [20]
    f_reraise RAISE [10], PY_UNWIND [10], RERAISE [10]
    test_profile RAISE [20]
    --- PY_START, PY_RETURN ---
    990
    f_cdef PY_START [10], PY_RETURN [10]
    f_cpdef PY_START [20], PY_RETURN [20]
    f_def PY_START [10], PY_RETURN [10]
    f_inline PY_START [10], PY_RETURN [10]
    f_inline_prof PY_START [10], PY_RETURN [10]
    f_nogil_prof PY_START [10], PY_RETURN [10]
    f_raise PY_START [20], PY_UNWIND [20]
    f_reraise PY_START [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_START [10], PY_RETURN [10]
    f_return_none PY_START [10], PY_RETURN [10]
    f_withgil_prof PY_START [10], PY_RETURN [10]
    m_cdef PY_START [10], PY_RETURN [10]
    m_classmethod PY_START [10], PY_RETURN [10]
    m_cpdef PY_START [20], PY_RETURN [20]
    m_def PY_START [20], PY_RETURN [20]
    m_staticmethod PY_START [10], PY_RETURN [10]
    test_profile PY_START [1], PY_RETURN [1]
    --- PY_START, RAISE ---
    990
    f_cdef PY_START [10]
    f_cpdef PY_START [20]
    f_def PY_START [10]
    f_inline PY_START [10]
    f_inline_prof PY_START [10]
    f_nogil_prof PY_START [10]
    f_raise PY_START [20], RAISE [20], PY_UNWIND [20]
    f_reraise PY_START [10], RAISE [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_START [10]
    f_return_none PY_START [10]
    f_withgil_prof PY_START [10]
    m_cdef PY_START [10]
    m_classmethod PY_START [10]
    m_cpdef PY_START [20]
    m_def PY_START [20]
    m_staticmethod PY_START [10]
    test_profile PY_START [1], RAISE [20]
    --- PY_RETURN, RAISE ---
    990
    f_cdef PY_RETURN [10]
    f_cpdef PY_RETURN [20]
    f_def PY_RETURN [10]
    f_inline PY_RETURN [10]
    f_inline_prof PY_RETURN [10]
    f_nogil_prof PY_RETURN [10]
    f_raise RAISE [20], PY_UNWIND [20]
    f_reraise RAISE [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_RETURN [10]
    f_return_none PY_RETURN [10]
    f_withgil_prof PY_RETURN [10]
    m_cdef PY_RETURN [10]
    m_classmethod PY_RETURN [10]
    m_cpdef PY_RETURN [20]
    m_def PY_RETURN [20]
    m_staticmethod PY_RETURN [10]
    test_profile PY_RETURN [1], RAISE [20]
    --- PY_START, PY_RETURN, RAISE ---
    990
    f_cdef PY_START [10], PY_RETURN [10]
    f_cpdef PY_START [20], PY_RETURN [20]
    f_def PY_START [10], PY_RETURN [10]
    f_inline PY_START [10], PY_RETURN [10]
    f_inline_prof PY_START [10], PY_RETURN [10]
    f_nogil_prof PY_START [10], PY_RETURN [10]
    f_raise PY_START [20], RAISE [20], PY_UNWIND [20]
    f_reraise PY_START [10], RAISE [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_START [10], PY_RETURN [10]
    f_return_none PY_START [10], PY_RETURN [10]
    f_withgil_prof PY_START [10], PY_RETURN [10]
    m_cdef PY_START [10], PY_RETURN [10]
    m_classmethod PY_START [10], PY_RETURN [10]
    m_cpdef PY_START [20], PY_RETURN [20]
    m_def PY_START [20], PY_RETURN [20]
    m_staticmethod PY_START [10], PY_RETURN [10]
    test_profile PY_START [1], PY_RETURN [1], RAISE [20]


    ## Testing generators:

    >>> with monitored_events(events=GEN_EVENTS, function_name='f_generator') as collected_events:
    ...     gen = f_generator()
    ...     for i in gen: print(i)
    1
    2
    >>> print_events(collected_events)  # f_generator
    f_generator PY_START [1], PY_RESUME [2], PY_RETURN [1], PY_YIELD [2]


    >>> with monitored_events(events=GEN_EVENTS, function_name='test_generators') as collected_events:
    ...     test_generators()
    >>> print_events(collected_events)  # test_generators()
    f_generator PY_START [1], PY_RESUME [2], PY_RETURN [1], PY_YIELD [2]
    f_generator_exception PY_START [1], PY_RESUME [1], PY_YIELD [1], RAISE [1]
    f_generator_expr PY_START [1], PY_RETURN [1]
    test_generators PY_START [1], PY_RETURN [1]


    ## Testing line events:

    >>> events = (E.PY_START, E.PY_RETURN)
    >>> for num_events in range(1, len(events)+1):  # doctest: +REPORT_NDIFF
    ...     for event_set in combinations(events, num_events):
    ...         event_set += (E.RAISE, E.LINE)
    ...         print(f"--- {names(event_set)} ---")
    ...         with monitored_events(events=event_set + (E.RERAISE, E.PY_UNWIND)) as (collected_events, collected_line_events):
    ...             result = test_profile(10)
    ...         print(result)
    ...         print_events(collected_events)
    ...         assert_events(event_set, collected_events['test_profile'])  # test_profile(10)
    --- PY_START, LINE, RAISE ---
    990
    f_cdef PY_START [10], LINE [10]
    f_cpdef PY_START [20], LINE [20]
    f_def PY_START [10], LINE [10]
    f_inline PY_START [10], LINE [10]
    f_inline_prof PY_START [10], LINE [10]
    f_nogil_prof PY_START [10], LINE [10]
    f_raise PY_START [20], LINE [20], RAISE [20], PY_UNWIND [20]
    f_reraise PY_START [10], LINE [50], RAISE [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_START [10], LINE [10]
    f_return_none PY_START [10], LINE [10]
    f_withgil_prof PY_START [10], LINE [10]
    m_cdef PY_START [10], LINE [10]
    m_classmethod PY_START [10], LINE [10]
    m_cpdef PY_START [20], LINE [20]
    m_def PY_START [20], LINE [20]
    m_staticmethod PY_START [10], LINE [10]
    test_profile PY_START [1], LINE [385], RAISE [20]
    --- PY_RETURN, LINE, RAISE ---
    990
    f_cdef PY_RETURN [10], LINE [10]
    f_cpdef PY_RETURN [20], LINE [20]
    f_def PY_RETURN [10], LINE [10]
    f_inline PY_RETURN [10], LINE [10]
    f_inline_prof PY_RETURN [10], LINE [10]
    f_nogil_prof PY_RETURN [10], LINE [10]
    f_raise LINE [20], RAISE [20], PY_UNWIND [20]
    f_reraise LINE [50], RAISE [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_RETURN [10], LINE [10]
    f_return_none PY_RETURN [10], LINE [10]
    f_withgil_prof PY_RETURN [10], LINE [10]
    m_cdef PY_RETURN [10], LINE [10]
    m_classmethod PY_RETURN [10], LINE [10]
    m_cpdef PY_RETURN [20], LINE [20]
    m_def PY_RETURN [20], LINE [20]
    m_staticmethod PY_RETURN [10], LINE [10]
    test_profile PY_RETURN [1], LINE [385], RAISE [20]
    --- PY_START, PY_RETURN, LINE, RAISE ---
    990
    f_cdef PY_START [10], PY_RETURN [10], LINE [10]
    f_cpdef PY_START [20], PY_RETURN [20], LINE [20]
    f_def PY_START [10], PY_RETURN [10], LINE [10]
    f_inline PY_START [10], PY_RETURN [10], LINE [10]
    f_inline_prof PY_START [10], PY_RETURN [10], LINE [10]
    f_nogil_prof PY_START [10], PY_RETURN [10], LINE [10]
    f_raise PY_START [20], LINE [20], RAISE [20], PY_UNWIND [20]
    f_reraise PY_START [10], LINE [50], RAISE [10], PY_UNWIND [10], RERAISE [10]
    f_return_default PY_START [10], PY_RETURN [10], LINE [10]
    f_return_none PY_START [10], PY_RETURN [10], LINE [10]
    f_withgil_prof PY_START [10], PY_RETURN [10], LINE [10]
    m_cdef PY_START [10], PY_RETURN [10], LINE [10]
    m_classmethod PY_START [10], PY_RETURN [10], LINE [10]
    m_cpdef PY_START [20], PY_RETURN [20], LINE [20]
    m_def PY_START [20], PY_RETURN [20], LINE [20]
    m_staticmethod PY_START [10], PY_RETURN [10], LINE [10]
    test_profile PY_START [1], PY_RETURN [1], LINE [385], RAISE [20]


    ## Testing fused functions:

    >>> with monitored_events(events=FUNC_EVENTS, function_name='call_fused_functions') as collected_events:
    ...     call_fused_functions()
    >>> print_events(collected_events)  # call_fused_functions()
    call_fused_functions PY_START [1], PY_RETURN [1]


    ## Testing special return types:

    >>> events = set()
    >>> def trace_return(code, offset, arg):
    ...     events.add(arg)

    >>> _ = smon.register_callback(TOOL_ID, E.PY_RETURN, trace_return)
    >>> smon.set_events(TOOL_ID, E.PY_RETURN)
    >>> try:
    ...     # monitored
    ...     trace_return_neg_1()
    ...     trace_return_charptr()
    ... finally:
    ...     _ = smon.register_callback(TOOL_ID, E.PY_RETURN, None)
    ...     smon.free_tool_id(TOOL_ID)
    -1
    b'xyzxyz'

    >>> -1 in events  or  events
    True
    >>> None in events  or  events
    True
    >>> b'xyzxyz' in events  or  events
    True
    >>> (b'xyz' not in events if COMPILED else b'xyz' in events)  or  events
    True


    >>> smon.free_tool_id(TOOL_ID)
    """


def names(event_ids):
    return ', '.join([event_name(1 << event_id) for event_id in sorted(event_ids)])


def print_events(collected_events):
    def event_sum(event_id, event_counts):
        count = sum(event_counts)
        if not cython.compiled and event_id == E.RERAISE and count == 20:
            # CPython bug, see https://github.com/python/cpython/issues/118360
            count //= 2
        return count

    for func_name, line_counts in sorted(collected_events.items()):
        print(func_name,
            ', '.join(f"{names([event_id])} [{event_sum(event_id, counts.values())}]" for event_id, counts in sorted(line_counts.items())))


def assert_events(expected_events, collected_events, loops=10):
    missing = set(expected_events).difference(collected_events)
    surplus = set(collected_events).difference(expected_events)

    if missing:
        print(f"Expected: [{names(expected_events)}], missing: [{names(missing)}]")
    if surplus:
        print(f"Expected: [{names(expected_events)}], surplus: [{names(surplus)}]")

    collected_events = {name: dict(values) for name, values in collected_events.items()}


@contextmanager
@cython.profile(False)
@cython.linetrace(False)
def monitored_events(events=FUNC_EVENTS, function_name="test_profile"):
    event_set = E.NO_EVENTS
    for event in events:
        event_set |= event

    collected_events = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    collected_line_events = defaultdict(int)

    @cython.profile(False)
    @cython.linetrace(False)
    def count_event(event, code_obj, offset, *args):
        if not (code_obj.co_name.startswith('f_') or code_obj.co_name.startswith('m_') or code_obj.co_name == function_name):
            return smon.DISABLE if event != E.RAISE else None
        if ' (wrapper)' in code_obj.co_name:
            return  # ignore cpdef wrapper
        if not cython.compiled and 'noprof' in code_obj.co_name:
            return smon.DISABLE if event != E.RAISE else None
        if event == E.LINE:
            # offset == line
            collected_line_events[offset] += 1
            assert offset in (line for line, *_ in code_obj.co_positions()), f"{code_obj.co_name}: {offset} in {list(code_obj.co_positions())}"
        collected_events[code_obj.co_name][event][offset] += 1

    try:
        for event in events:
            smon.register_callback(TOOL_ID, event, partial(count_event, event))
        smon.set_events(TOOL_ID, event_set)
        if event_set & E.LINE:
            yield collected_events, collected_line_events
        else:
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
    a: CyA = CyA()
    py_a = PyA()

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

        retval = f_return_none(i)
        assert retval is None, retval
        retval = f_return_default(i)
        assert retval == (0 if cython.compiled else None), retval

        n += a.m_def(i)
        obj = a
        n += obj.m_def(i)
        n += a.m_cpdef(i)
        n += obj.m_cpdef(i)
        n += a.m_cdef(i)
        n += CyA.m_staticmethod(i)
        n += a.m_classmethod(i)

        n += py_a.pym_def(i)
        obj = py_a
        n += obj.pym_def(i)
        n += py_a.pym_staticmethod(i)
        n += py_a.pym_classmethod(i)

        try:
            n += f_raise(i+2)
        except RuntimeError:
            pass
        try:
            n += f_reraise(i+2)
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

@cython.exceptval(-2)
@cython.cfunc
def f_reraise(a: cython.long) -> cython.long:
    try:
        f_raise(a)
    except ValueError:
        pass
    except RuntimeError:
        raise

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

@cython.ccall
def f_return_none(_: cython.long):
    pass

@cython.ccall
def f_return_default(_: cython.long) -> cython.long:
    pass


@cython.cclass
class CyA:
    def m_def(self, a: cython.long):
        return a

    @cython.ccall
    def m_cpdef(self, a: cython.long):
        return a

    @cython.cfunc
    def m_cdef(self, a: cython.long) -> cython.long:
        return a

    @classmethod
    @cython.cfunc
    def m_classmethod(cls, a: cython.long) -> cython.long:
        return a

    @staticmethod
    @cython.cfunc
    def m_staticmethod(a: cython.long) -> cython.long:
        return a


class PyA:
    def pym_def(self, a: cython.long):
        return a

    @classmethod
    def pym_classmethod(cls, a: cython.long) -> cython.long:
        return a

    @staticmethod
    def pym_staticmethod(a: cython.long) -> cython.long:
        return a


# Generators

def test_generators(_=None):
    call_generator()
    call_generator_exception()
    f_generator_expr()

def call_generator():
    list(f_generator())

def f_generator():
    yield 1
    yield 2

def call_generator_exception():
    try:
        list(f_generator_exception())
    except ValueError:
        pass

def f_generator_exception():
    yield 1
    raise ValueError(2)

def f_generator_expr():
    e = (x for x in range(10))
    return sum(e)


# Fused functions

def call_fused_functions():
    if cython.compiled:
        assert 5 == fused_func_def['short'](3)
        assert 5 == fused_func_def['int'](3)
        assert 5 == fused_func_def['double'](3)
        assert 5 == fused_func_def['float'](3)
        assert 5 == fused_func_def['long'](3)

    assert 5.0 == fused_func_def(3.0)
    assert 5 == fused_func_def(3)

    if cython.compiled:
        assert 5 == fused_func_cfunc[cython.short](3)
        assert 5 == fused_func_cfunc[cython.int](3)
        assert 5 == fused_func_cfunc[cython.double](3)
        assert 5 == fused_func_cfunc[cython.float](3)
        assert 5 == fused_func_cfunc[cython.long](3)

    assert 5.0 == fused_func_cfunc(3.0)
    assert 5 == fused_func_cfunc(3)


def fused_func_def(x: cython.numeric) -> cython.numeric:
    return x + 2

@cython.cfunc
def fused_func_cfunc(x: cython.numeric) -> cython.numeric:
    return x + 2


# Special return values

@cython.cfunc
def c_return_neg_1() -> cython.Py_UCS4:
    # Returning an invalid Py_UCS4 value could fail in combination with trace result reporting.
    # See https://github.com/cython/cython/issues/6503
    return cython.cast(cython.Py_UCS4, -1)

def call_c_return_neg_1():
    return cython.cast(cython.int, c_return_neg_1())

def trace_return_neg_1():
    result = call_c_return_neg_1()
    return result


@cython.cfunc
def c_return_charptr() -> cython.p_char:
    return b"xyz"

def trace_return_charptr():
    result: object = c_return_charptr()
    return result * 2
