# cython: auto_cpdef=True, language_level=3
# mode: run
# tag: directive,auto_cpdef,generators

"""
Module-level generator functions are promotable to cpdef/ccall with auto_cpdef=True.
The C-level __pyx_f_ function just calls the Python __pyx_pf_ which creates the
generator object; all generator semantics (yield, send, throw, close) work as usual.
"""

import cython
from typing import Iterator

# --- Plain generator, auto-promoted ---
def generator_func():
    """
    >>> list(generator_func())
    [1, 2]
    >>> g = generator_func()
    >>> next(g)
    1
    >>> next(g)
    2
    >>> next(g)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    yield 1
    yield 2


# --- Typed-arg generator ---
def gen_typed(n: cython.int):
    """
    >>> list(gen_typed(3))
    [0, 1, 2]
    >>> list(gen_typed(0))
    []
    """
    for i in range(n):
        yield i


# --- Auto-promoted generator with a yield-type annotation (all compatible) ---
def gen_annotated(n: cython.int) -> Iterator[int]:
    """
    >>> list(gen_annotated(3))
    [0, 1, 2]
    """
    i: cython.int
    for i in range(n):
        yield i


def gen_annotated_chain(n: cython.int) -> Iterator[int]:
    """yield from a promoted annotated generator with a compatible item type.
    >>> list(gen_annotated_chain(2))
    [0, 1, -1]
    """
    yield from gen_annotated(n)
    yield -1


# --- Generator with default arguments ---
def gen_with_defaults(a: cython.int = 3, b=None):
    """
    >>> list(gen_with_defaults())
    [0, 1, 2]
    >>> list(gen_with_defaults(2))
    [0, 1]
    >>> list(gen_with_defaults(2, 'x'))
    ['x', 'x']
    """
    for i in range(a):
        yield b if b is not None else i


# --- Generator with closure inside (lambda) ---
def gen_with_closure(n: cython.int):
    """
    >>> list(gen_with_closure(3))
    [0, 2, 4]
    """
    double = lambda x: x * 2
    for i in range(n):
        yield double(i)


# --- Same-module cpdef call to promoted generator ---
# The call inside call_generator should compile to a C-level __pyx_f_ call.
@cython.test_assert_path_exists('//SimpleCallNode[@function.type.is_cfunction = True]')
def call_generator():
    """
    >>> list(call_generator())
    [1, 2]
    """
    return generator_func()


# --- Explicit @cython.ccall form ---
@cython.ccall
def gen_explicit(x: cython.int):
    """
    >>> list(gen_explicit(4))
    [0, 1, 2, 3]
    """
    for i in range(x):
        yield i


# --- send/throw/close on promoted generator ---
def test_send():
    """
    >>> test_send()
    1
    2
    """
    g = generator_func()
    print(g.send(None))   # same as next(g)
    print(g.send(None))   # same as next(g)


def test_throw():
    """
    >>> test_throw()
    caught
    """
    g = generator_func()
    next(g)
    try:
        g.throw(ValueError, "test")
    except ValueError:
        print("caught")


def test_close():
    """
    >>> test_close()
    closed
    """
    g = generator_func()
    next(g)
    g.close()
    print("closed")


# --- Exception raised inside the generator body (depth 1) ---
def gen_raises(n: cython.int):
    """The promoted generator's body raises after exhausting its yields.

    >>> g = gen_raises(2)
    >>> next(g), next(g)
    (0, 1)
    >>> next(g)
    Traceback (most recent call last):
    ...
    ValueError: boom at 2
    >>> next(gen_raises(0))
    Traceback (most recent call last):
    ...
    ValueError: boom at 0
    """
    i: cython.int
    for i in range(n):
        yield i
    raise ValueError("boom at %d" % n)


# --- Exception propagated through two generator levels (yield from) ---
def gen_raises_nested(n: cython.int):
    """Outer promoted generator delegates to an inner promoted generator
    whose body raises; the exception propagates through both levels.

    >>> g = gen_raises_nested(2)
    >>> next(g), next(g)
    (0, 1)
    >>> next(g)
    Traceback (most recent call last):
    ...
    ValueError: boom at 2
    """
    yield from gen_raises(n)


def gen_raises_nested_loop(n: cython.int):
    """Same two-level propagation but re-yielding through an explicit loop
    instead of yield from.

    >>> list(gen_raises_nested_loop(1))
    Traceback (most recent call last):
    ...
    ValueError: boom at 1
    """
    for v in gen_raises(n):
        yield v


# --- Two-level exception consumed from a promoted cpdef function (C-call path) ---
def consume_nested_raises(n: cython.int):
    """The call to gen_raises_nested() compiles to a C call into the trampoline;
    the inner generator's exception must surface intact through both generator
    frames into the C caller.

    >>> consume_nested_raises(3)
    ('caught', 'boom at 3', [0, 1, 2])
    """
    out = []
    try:
        for v in gen_raises_nested(n):
            out.append(v)
    except ValueError as exc:
        return ('caught', str(exc), out)


# --- Async def is NOT promoted (stays as Python def) ---
async def async_gen():
    yield 1


# --- Star-arg generators are NOT promoted ---
def stararg_gen(*args):
    """
    >>> list(stararg_gen(1, 2))
    [1, 2]
    """
    for x in args:
        yield x
