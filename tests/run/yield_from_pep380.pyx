# -*- coding: utf-8 -*-

"""
Test suite for PEP 380 implementation

adapted from original tests written by Greg Ewing
see <http://www.cosc.canterbury.ac.nz/greg.ewing/python/yield-from/YieldFrom-Python3.1.2-rev5.zip>
"""

import sys


def _lines(trace):
    for line in trace:
        print(line)


def test_delegation_of_initial_next_to_subgenerator():
    """
    >>> _lines(test_delegation_of_initial_next_to_subgenerator())
    Starting g1
    Starting g2
    Yielded 42
    Finishing g2
    Finishing g1
    """
    trace = []
    def g1():
        trace.append("Starting g1")
        yield from g2()
        trace.append("Finishing g1")
    def g2():
        trace.append("Starting g2")
        yield 42
        trace.append("Finishing g2")
    for x in g1():
        trace.append("Yielded %s" % (x,))
    return trace

def test_raising_exception_in_initial_next_call():
    """
    >>> _lines(test_raising_exception_in_initial_next_call())
    Starting g1
    Starting g2
    Finishing g2
    Finishing g1
    """
    trace = []
    def g1():
        try:
            trace.append("Starting g1")
            yield from g2()
        finally:
            trace.append("Finishing g1")
    def g2():
        try:
            trace.append("Starting g2")
            raise ValueError("spanish inquisition occurred")
        finally:
            trace.append("Finishing g2")
    try:
        for x in g1():
            trace.append("Yielded %s" % (x,))
    except ValueError as e:
        pass
    else:
        trace.append("subgenerator failed to raise ValueError")
    return trace

def test_delegation_of_next_call_to_subgenerator():
    """
    >>> _lines(test_delegation_of_next_call_to_subgenerator())
    Starting g1
    Yielded g1 ham
    Starting g2
    Yielded g2 spam
    Yielded g2 more spam
    Finishing g2
    Yielded g1 eggs
    Finishing g1
    """
    trace = []
    def g1():
        trace.append("Starting g1")
        yield "g1 ham"
        yield from g2()
        yield "g1 eggs"
        trace.append("Finishing g1")
    def g2():
        trace.append("Starting g2")
        yield "g2 spam"
        yield "g2 more spam"
        trace.append("Finishing g2")
    for x in g1():
        trace.append("Yielded %s" % (x,))
    return trace

def test_raising_exception_in_delegated_next_call():
    """
    >>> _lines(test_raising_exception_in_delegated_next_call())
    Starting g1
    Yielded g1 ham
    Starting g2
    Yielded g2 spam
    Finishing g2
    Finishing g1
    """
    trace = []
    def g1():
        try:
            trace.append("Starting g1")
            yield "g1 ham"
            yield from g2()
            yield "g1 eggs"
        finally:
            trace.append("Finishing g1")
    def g2():
        try:
            trace.append("Starting g2")
            yield "g2 spam"
            raise ValueError("hovercraft is full of eels")
            yield "g2 more spam"
        finally:
            trace.append("Finishing g2")
    try:
        for x in g1():
            trace.append("Yielded %s" % (x,))
    except ValueError:
        pass
    else:
        trace.append("subgenerator failed to raise ValueError")
    return trace

def test_delegation_of_send():
    """
    >>> _lines(test_delegation_of_send())
    Starting g1
    g1 received 1
    Starting g2
    Yielded g2 spam
    g2 received 2
    Yielded g2 more spam
    g2 received 3
    Finishing g2
    Yielded g1 eggs
    g1 received 4
    Finishing g1
    """
    trace = []
    def g1():
        trace.append("Starting g1")
        x = yield "g1 ham"
        trace.append("g1 received %s" % (x,))
        yield from g2()
        x = yield "g1 eggs"
        trace.append("g1 received %s" % (x,))
        trace.append("Finishing g1")
    def g2():
        trace.append("Starting g2")
        x = yield "g2 spam"
        trace.append("g2 received %s" % (x,))
        x = yield "g2 more spam"
        trace.append("g2 received %s" % (x,))
        trace.append("Finishing g2")
    g = g1()
    y = next(g)
    x = 1
    try:
        while 1:
            y = g.send(x)
            trace.append("Yielded %s" % (y,))
            x += 1
    except StopIteration:
        pass
    return trace

def test_handling_exception_while_delegating_send():
    """
    >>> _lines(test_handling_exception_while_delegating_send())
    Starting g1
    g1 received 1
    Starting g2
    Yielded g2 spam
    g2 received 2
    """
    trace = []
    def g1():
        trace.append("Starting g1")
        x = yield "g1 ham"
        trace.append("g1 received %s" % (x,))
        yield from g2()
        x = yield "g1 eggs"
        trace.append("g1 received %s" % (x,))
        trace.append("Finishing g1")
    def g2():
        trace.append("Starting g2")
        x = yield "g2 spam"
        trace.append("g2 received %s" % (x,))
        raise ValueError("hovercraft is full of eels")
        x = yield "g2 more spam"
        trace.append("g2 received %s" % (x,))
        trace.append("Finishing g2")
    def run():
        g = g1()
        y = next(g)
        x = 1
        try:
            while 1:
                y = g.send(x)
                trace.append("Yielded %s" % (y,))
                x += 1
        except StopIteration:
            trace.append("StopIteration")
    try:
        run()
    except ValueError:
        pass # ok
    else:
        trace.append("no ValueError")
    return trace

def test_delegating_close():
    """
    >>> _lines(test_delegating_close())
    Starting g1
    Yielded g1 ham
    Starting g2
    Yielded g2 spam
    Finishing g2
    Finishing g1
    """
    trace = []
    def g1():
        try:
            trace.append("Starting g1")
            yield "g1 ham"
            yield from g2()
            yield "g1 eggs"
        finally:
            trace.append("Finishing g1")
    def g2():
        try:
            trace.append("Starting g2")
            yield "g2 spam"
            yield "g2 more spam"
        finally:
            trace.append("Finishing g2")
    g = g1()
    for i in range(2):
        x = next(g)
        trace.append("Yielded %s" % (x,))
    g.close()
    return trace

def test_handing_exception_while_delegating_close():
    """
    >>> _lines(test_handing_exception_while_delegating_close())
    Starting g1
    Yielded g1 ham
    Starting g2
    Yielded g2 spam
    Finishing g2
    Finishing g1
    nybbles have exploded with delight
    """
    trace = []
    def g1():
        try:
            trace.append("Starting g1")
            yield "g1 ham"
            yield from g2()
            yield "g1 eggs"
        finally:
            trace.append("Finishing g1")
    def g2():
        try:
            trace.append("Starting g2")
            yield "g2 spam"
            yield "g2 more spam"
        finally:
            trace.append("Finishing g2")
            raise ValueError("nybbles have exploded with delight")
    try:
        g = g1()
        for i in range(2):
            x = next(g)
            trace.append("Yielded %s" % (x,))
        g.close()
    except ValueError as e:
        trace.append(e.args[0])
        # FIXME: __context__ is currently not set
        #if sys.version_info[0] >= 3:
        #    assert isinstance(e.__context__, GeneratorExit), 'exception context is %r' % e.__context__
    else:
        trace.append("subgenerator failed to raise ValueError")
    return trace

def test_delegating_throw():
    """
    >>> _lines(test_delegating_throw())
    Starting g1
    Yielded g1 ham
    Starting g2
    Yielded g2 spam
    Finishing g2
    Finishing g1
    """
    trace = []
    def g1():
        try:
            trace.append("Starting g1")
            yield "g1 ham"
            yield from g2()
            yield "g1 eggs"
        finally:
            trace.append("Finishing g1")
    def g2():
        try:
            trace.append("Starting g2")
            yield "g2 spam"
            yield "g2 more spam"
        finally:
            trace.append("Finishing g2")
    try:
        g = g1()
        for i in range(2):
            x = next(g)
            trace.append("Yielded %s" % (x,))
        e = ValueError("tomato ejected")
        g.throw(e)
    except ValueError:
        pass
    else:
        trace.append("subgenerator failed to raise ValueError")
    return trace

def __test_value_attribute_of_StopIteration_exception():
    """
    StopIteration:
    value = None
    StopIteration: spam
    value = spam
    StopIteration: spam
    value = eggs
    """
    trace = []
    def pex(e):
        trace.append("%s: %s" % (e.__class__.__name__, e))
        trace.append("value = %s" % (e.value,))
    e = StopIteration()
    pex(e)
    e = StopIteration("spam")
    pex(e)
    e.value = "eggs"
    pex(e)
    return trace


def test_exception_value_crash():
    """
    >>> test_exception_value_crash()
    ['g2']
    """
    # There used to be a refcount error in CPython when the return value
    # stored in the StopIteration has a refcount of 1.
    def g1():
        yield from g2()
    def g2():
        yield "g2"
        return [42]
    return list(g1())


def test_return_none():
    """
    >>> test_return_none()
    ['g2']
    """
    # There used to be a refcount error in CPython when the return value
    # stored in the StopIteration has a refcount of 1.
    def g1():
        yield from g2()
    def g2():
        yield "g2"
        return None
    return list(g1())


def test_finally_return_none(raise_exc=None):
    """
    >>> gen = test_finally_return_none()
    >>> next(gen)
    'g2'
    >>> next(gen)
    Traceback (most recent call last):
    StopIteration

    >>> gen = test_finally_return_none()
    >>> next(gen)
    'g2'
    >>> try: gen.throw(ValueError())
    ... except StopIteration: pass
    ... else: print("FAILED")
    """
    # There used to be a refcount error in CPython when the return value
    # stored in the StopIteration has a refcount of 1.
    def g1():
        yield from g2()
    def g2():
        try:
            yield "g2"
        finally:
            return None
    return g1()


def test_generator_return_value():
    """
    >>> _lines(test_generator_return_value())
    Starting g1
    Yielded g1 ham
    Starting g2
    Yielded g2 spam
    Yielded g2 more spam
    Finishing g2
    g2 returned None
    Starting g2
    Yielded g2 spam
    Yielded g2 more spam
    Finishing g2
    g2 returned 42
    Yielded g1 eggs
    Finishing g1
    """
    trace = []
    def g1():
        trace.append("Starting g1")
        yield "g1 ham"
        ret = yield from g2()
        trace.append("g2 returned %s" % (ret,))
        ret = yield from g2(42)
        trace.append("g2 returned %s" % (ret,))
        yield "g1 eggs"
        trace.append("Finishing g1")
    def g2(v = None):
        trace.append("Starting g2")
        yield "g2 spam"
        yield "g2 more spam"
        trace.append("Finishing g2")
        if v:
            return v
    for x in g1():
        trace.append("Yielded %s" % (x,))
    return trace

def test_delegation_of_next_to_non_generator():
    """
    >>> _lines(test_delegation_of_next_to_non_generator())
    Yielded 0
    Yielded 1
    Yielded 2
    """
    trace = []
    def g():
        yield from range(3)
    for x in g():
        trace.append("Yielded %s" % (x,))
    return trace

def test_conversion_of_sendNone_to_next():
    """
    >>> _lines(test_conversion_of_sendNone_to_next())
    Yielded: 0
    Yielded: 1
    Yielded: 2
    """
    trace = []
    def g():
        yield from range(3)
    gi = g()
    for x in range(3):
        y = gi.send(None)
        trace.append("Yielded: %s" % (y,))
    return trace

def test_delegation_of_close_to_non_generator():
    """
    >>> _lines(test_delegation_of_close_to_non_generator())
    starting g
    finishing g
    """
    trace = []
    def g():
        try:
            trace.append("starting g")
            yield from range(3)
            trace.append("g should not be here")
        finally:
            trace.append("finishing g")
    gi = g()
    next(gi)
    gi.close()
    return trace

def test_delegating_throw_to_non_generator():
    """
    >>> _lines(test_delegating_throw_to_non_generator())
    Starting g
    Yielded 0
    Yielded 1
    Yielded 2
    Yielded 3
    Yielded 4
    Finishing g
    """
    trace = []
    def g():
        try:
            trace.append("Starting g")
            yield from range(10)
        finally:
            trace.append("Finishing g")
    try:
        gi = g()
        for i in range(5):
            x = next(gi)
            trace.append("Yielded %s" % (x,))
        e = ValueError("tomato ejected")
        gi.throw(e)
    except ValueError:
        pass
    else:
        trace.append("subgenerator failed to raise ValueError")
    return trace

def test_attempting_to_send_to_non_generator():
    """
    >>> _lines(test_attempting_to_send_to_non_generator())
    starting g
    finishing g
    """
    trace = []
    def g():
        try:
            trace.append("starting g")
            yield from range(3)
            trace.append("g should not be here")
        finally:
            trace.append("finishing g")
    try:
        gi = g()
        next(gi)
        for x in range(3):
            y = gi.send(42)
            trace.append("Should not have yielded: %s" % y)
    except AttributeError:
        pass
    else:
        trace.append("was able to send into non-generator")
    return trace

def test_broken_getattr_handling():
    """
    >>> test_broken_getattr_handling()
    []
    """
    class Broken:
        def __iter__(self):
            return self
        def __next__(self):
            return 1
        next = __next__
        def __getattr__(self, attr):
            1/0

    def g():
        yield from Broken()

    not_raised = []
    try:
        gi = g()
        assert next(gi) == 1
        gi.send(1)
    except ZeroDivisionError:
        pass
    else:
        not_raised.append(1)

    try:
        gi = g()
        assert next(gi) == 1
        gi.throw(AttributeError)
    except ZeroDivisionError:
        pass
    else:
        not_raised.append(2)

    """
    # this currently only calls PyErr_WriteUnraisable() and doesn't raise ...
    try:
        gi = g()
        assert next(gi) == 1
        gi.close()
    except ZeroDivisionError:
        pass
    else:
        not_raised.append(3)
    """
    gi = g()
    assert next(gi) == 1
    gi.close()

    return not_raised

def test_exception_in_initial_next_call():
    """
    >>> _lines(test_exception_in_initial_next_call())
    g1 about to yield from g2
    """
    trace = []
    def g1():
        trace.append("g1 about to yield from g2")
        yield from g2()
        trace.append("g1 should not be here")
    def g2():
        yield 1/0
    def run():
        gi = g1()
        next(gi)
    try:
        run()
    except ZeroDivisionError:
        pass
    else:
        trace.append("ZeroDivisionError not raised")
    return trace

def test_attempted_yield_from_loop():
    """
    >>> _lines(test_attempted_yield_from_loop())
    g1: starting
    Yielded: y1
    g1: about to yield from g2
    g2: starting
    Yielded: y2
    g2: about to yield from g1
    """
    trace = []
    def g1():
        trace.append("g1: starting")
        yield "y1"
        trace.append("g1: about to yield from g2")
        yield from g2()
        trace.append("g1 should not be here")

    def g2():
        trace.append("g2: starting")
        yield "y2"
        trace.append("g2: about to yield from g1")
        yield from gi
        trace.append("g2 should not be here")
    try:
        gi = g1()
        for y in gi:
            trace.append("Yielded: %s" % (y,))
    except ValueError:
        pass # "generator already executing"
    else:
        trace.append("subgenerator didn't raise ValueError")
    return trace

def test_attempted_reentry():
    """
    >>> _lines(test_attempted_reentry())
    g1: starting
    Yielded: y1
    g1: about to yield from g2
    g2: starting
    Yielded: y2
    g2: about to yield from g1
    g2: caught ValueError
    Yielded: y3
    g1: after delegating to g2
    Yielded: y4
    """
    trace = []
    def g1():
        trace.append("g1: starting")
        yield "y1"
        trace.append("g1: about to yield from g2")
        yield from g2()
        trace.append("g1: after delegating to g2")
        yield "y4"

    def g2():
        trace.append("g2: starting")
        yield "y2"
        trace.append("g2: about to yield from g1")
        try:
            yield from gi
        except ValueError:
            trace.append("g2: caught ValueError")
        else:
            trace.append("g1 did not raise ValueError on reentry")
        yield "y3"
    gi = g1()
    for y in gi:
        trace.append("Yielded: %s" % (y,))
    return trace

def test_returning_value_from_delegated_throw():
    """
    >>> _lines(test_returning_value_from_delegated_throw())
    Starting g1
    Yielded g1 ham
    Starting g2
    Yielded g2 spam
    Caught LunchError in g2
    Yielded g2 yet more spam
    Yielded g1 eggs
    Finishing g1
    """
    trace = []
    def g1():
        try:
            trace.append("Starting g1")
            yield "g1 ham"
            yield from g2()
            yield "g1 eggs"
        finally:
            trace.append("Finishing g1")
    def g2():
        try:
            trace.append("Starting g2")
            yield "g2 spam"
            yield "g2 more spam"
        except LunchError:
            trace.append("Caught LunchError in g2")
            yield "g2 lunch saved"
            yield "g2 yet more spam"
    class LunchError(Exception):
        pass
    g = g1()
    for i in range(2):
        x = next(g)
        trace.append("Yielded %s" % (x,))
    e = LunchError("tomato ejected")
    g.throw(e)
    for x in g:
        trace.append("Yielded %s" % (x,))
    return trace

def test_next_and_return_with_value():
    """
    >>> _lines(test_next_and_return_with_value())
    g starting
    f resuming g
    g returning None
    f caught StopIteration
    g starting
    f resuming g
    g returning 42
    f caught StopIteration
    """
    trace = []
    def f(r):
        gi = g(r)
        next(gi)
        try:
            trace.append("f resuming g")
            next(gi)
            trace.append("f SHOULD NOT BE HERE")
        except StopIteration:
            trace.append("f caught StopIteration")
    def g(r):
        trace.append("g starting")
        yield
        trace.append("g returning %s" % (r,))
        return r
    f(None)
    f(42)
    return trace

def test_send_and_return_with_value():
    """
    >>> _lines(test_send_and_return_with_value())
    g starting
    f sending spam to g
    g received spam
    g returning None
    f caught StopIteration
    g starting
    f sending spam to g
    g received spam
    g returning 42
    f caught StopIteration
    """
    trace = []
    def f(r):
        gi = g(r)
        next(gi)
        try:
            trace.append("f sending spam to g")
            gi.send("spam")
            trace.append("f SHOULD NOT BE HERE")
        except StopIteration:
            trace.append("f caught StopIteration")
    def g(r):
        trace.append("g starting")
        x = yield
        trace.append("g received %s" % (x,))
        trace.append("g returning %s" % (r,))
        return r
    f(None)
    f(42)
    return trace

def test_catching_exception_from_subgen_and_returning():
    """
    Test catching an exception thrown into a
    subgenerator and returning a value

    >>> _lines(test_catching_exception_from_subgen_and_returning())
    1
    inner caught ValueError
    inner returned 2 to outer
    2
    """
    trace = []
    def inner():
        try:
            yield 1
        except ValueError:
            trace.append("inner caught ValueError")
        return 2

    def outer():
        v = yield from inner()
        trace.append("inner returned %r to outer" % v)
        yield v
    g = outer()
    trace.append(next(g))
    trace.append(g.throw(ValueError))
    return trace

def test_throwing_GeneratorExit_into_subgen_that_returns():
    """
    Test throwing GeneratorExit into a subgenerator that
    catches it and returns normally.

    >>> _lines(test_throwing_GeneratorExit_into_subgen_that_returns())
    Enter g
    Enter f
    """
    trace = []
    def f():
        try:
            trace.append("Enter f")
            yield
            trace.append("Exit f")
        except GeneratorExit:
            return
    def g():
        trace.append("Enter g")
        yield from f()
        trace.append("Exit g")
    try:
        gi = g()
        next(gi)
        gi.throw(GeneratorExit)
    except GeneratorExit:
        pass
    else:
        trace.append("subgenerator failed to raise GeneratorExit")
    return trace

def test_throwing_GeneratorExit_into_subgenerator_that_yields():
    """
    Test throwing GeneratorExit into a subgenerator that
    catches it and yields.

    >>> _lines(test_throwing_GeneratorExit_into_subgenerator_that_yields())
    Enter g
    Enter f
    """
    trace = []
    def f():
        try:
            trace.append("Enter f")
            yield
            trace.append("Exit f")
        except GeneratorExit:
            yield
    def g():
        trace.append("Enter g")
        yield from f()
        trace.append("Exit g")
    try:
        gi = g()
        next(gi)
        gi.throw(GeneratorExit)
    except RuntimeError:
        pass # "generator ignored GeneratorExit"
    else:
        trace.append("subgenerator failed to raise GeneratorExit")
    return trace

def test_throwing_GeneratorExit_into_subgen_that_raises():
    """
    Test throwing GeneratorExit into a subgenerator that
    catches it and raises a different exception.

    >>> _lines(test_throwing_GeneratorExit_into_subgen_that_raises())
    Enter g
    Enter f
    """
    trace = []
    def f():
        try:
            trace.append("Enter f")
            yield
            trace.append("Exit f")
        except GeneratorExit:
            raise ValueError("Vorpal bunny encountered")
    def g():
        trace.append("Enter g")
        yield from f()
        trace.append("Exit g")
    try:
        gi = g()
        next(gi)
        gi.throw(GeneratorExit)
    except ValueError:
        pass # "Vorpal bunny encountered"
    else:
        trace.append("subgenerator failed to raise ValueError")
    return trace

def test_yield_from_empty():
    """
    >>> test_yield_from_empty()
    """
    def g():
        yield from ()
    try:
        next(g())
    except StopIteration:
        pass
    else:
        return "FAILED"

# test re-entry guards

def _reentering_gen():
    def one():
        yield 0
        yield from two()
        yield 3
    def two():
        yield 1
        try:
            yield from g1
        except ValueError:
            pass
        yield 2
    g1 = one()
    return g1

def test_delegating_generators_claim_to_be_running_next():
    """
    >>> test_delegating_generators_claim_to_be_running_next()
    [0, 1, 2, 3]
    """
    return list(_reentering_gen())

def test_delegating_generators_claim_to_be_running_send():
    """
    >>> test_delegating_generators_claim_to_be_running_send()
    [0, 1, 2, 3]
    """
    g1 = _reentering_gen()
    res = [next(g1)]
    try:
        while True:
            res.append(g1.send(42))
    except StopIteration:
        pass
    return res

def test_delegating_generators_claim_to_be_running_throw():
    """
    >>> test_delegating_generators_claim_to_be_running_throw()
    [0, 1, 2, 3]
    """
    class MyErr(Exception):
        pass
    def one():
        try:
            yield 0
        except MyErr:
            pass
        yield from two()
        try:
            yield 3
        except MyErr:
            pass
    def two():
        try:
            yield 1
        except MyErr:
            pass
        try:
            yield from g1
        except ValueError:
            pass
        try:
            yield 2
        except MyErr:
            pass
    g1 = one()
    res = [next(g1)]
    try:
        while True:
            res.append(g1.throw(MyErr))
    except StopIteration:
        pass
    return res

def test_delegating_generators_claim_to_be_running_close():
    """
    >>> test_delegating_generators_claim_to_be_running_close()
    42
    """
    class MyIt(object):
        def __iter__(self):
            return self
        def __next__(self):
            return 42
        next = __next__
        def close(self):
            assert g1.gi_running
            try:
                next(g1)
            except ValueError:
                pass # guard worked
            else:
                assert False, "re-entry guard failed to bark"
    def one():
        yield from MyIt()
    g1 = one()
    ret = next(g1)
    g1.close()
    return ret


def yield_in_return(x):
    """
    >>> x = yield_in_return(range(3))
    >>> for _ in range(10):
    ...     try:
    ...         print(next(x))
    ...     except StopIteration:
    ...         if sys.version_info >= (3,3):
    ...             print(sys.exc_info()[1].value is None)
    ...         else:
    ...             print(True)
    ...         break
    0
    1
    2
    True
    """
    return (yield from x)


def gi_yieldfrom(it):
    """
    >>> it = iter([1, 2, 3])
    >>> g = gi_yieldfrom(it)
    >>> g.gi_yieldfrom is None or "ERROR: %r" % g.gi_yieldfrom
    True
    >>> next(g)
    1
    >>> g.gi_yieldfrom is it or "ERROR: %r" % g.gi_yieldfrom
    True
    """
    x = yield from it
    return x
