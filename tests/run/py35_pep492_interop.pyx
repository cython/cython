# cython: language_level=3, binding=True
# mode: run
# tag: pep492, asyncfor, await


def run_async(coro, ignore_type=False):
    if not ignore_type:
        #assert coro.__class__ is types.GeneratorType
        assert coro.__class__.__name__ in ('coroutine', 'GeneratorWrapper'), coro.__class__.__name__

    buffer = []
    result = None
    while True:
        try:
            buffer.append(coro.send(None))
        except StopIteration as ex:
            result = ex.args[0] if ex.args else None
            break
    return buffer, result


def run_async__await__(coro):
    assert coro.__class__.__name__ in ('coroutine', 'GeneratorWrapper'), coro.__class__.__name__
    aw = coro.__await__()
    buffer = []
    result = None
    i = 0
    while True:
        try:
            if i % 2:
                buffer.append(next(aw))
            else:
                buffer.append(aw.send(None))
            i += 1
        except StopIteration as ex:
            result = ex.args[0] if ex.args else None
            break
    return buffer, result


async def await_pyobject(awaitable):
    """
    >>> async def simple():
    ...     return 10

    >>> buffer, result = run_async(await_pyobject(simple()))
    >>> result
    10

    >>> async def awaiting(awaitable):
    ...     return await awaitable

    >>> buffer, result = run_async(await_pyobject(awaiting(simple())))
    >>> result
    10
    """
    return await awaitable


def await_cyobject():
    """
    >>> async def run_await(awaitable):
    ...     return await awaitable

    >>> simple, awaiting = await_cyobject()

    >>> buffer, result = run_async(run_await(simple()))
    >>> result
    10

    >>> buffer, result = run_async(run_await(awaiting(simple())))
    >>> result
    10

    >>> buffer, result = run_async(run_await(awaiting(awaiting(simple()))))
    >>> result
    10

    >>> buffer, result = run_async(run_await(awaiting(run_await(awaiting(simple())))))
    >>> result
    10
    """

    async def simple():
        return 10

    async def awaiting(awaitable):
        return await awaitable

    return simple, awaiting


cimport cython

def yield_from_cyobject():
    """
    >>> async def py_simple_nonit():
    ...     return 10

    >>> async def run_await(awaitable):
    ...     return await awaitable

    >>> def run_yield_from(it):
    ...     return (yield from it)

    >>> simple_nonit, simple_it, awaiting, yield_from = yield_from_cyobject()

    >>> buffer, result = run_async(run_await(simple_it()))
    >>> result
    10
    >>> buffer, result = run_async(run_await(awaiting(simple_it())))
    >>> result
    10
    >>> buffer, result = run_async(awaiting(run_await(simple_it())), ignore_type=True)
    >>> result
    10
    >>> buffer, result = run_async(run_await(py_simple_nonit()))
    >>> result
    10

    >>> buffer, result = run_async(run_yield_from(awaiting(run_await(simple_it()))), ignore_type=True)
    >>> result
    10

    >>> buffer, result = run_async(run_yield_from(simple_it()), ignore_type=True)
    >>> result
    10
    >>> buffer, result = run_async(yield_from(simple_it()), ignore_type=True)
    >>> result
    10

    >>> next(run_yield_from(simple_nonit()))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> next(run_yield_from(py_simple_nonit()))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> next(yield_from(py_simple_nonit()))
    Traceback (most recent call last):
    TypeError: 'coroutine' object is not iterable
    """
    async def simple_nonit():
        return 10

    @cython.iterable_coroutine
    async def simple_it():
        return 10

    @cython.iterable_coroutine
    async def awaiting(awaitable):
        return await awaitable

    def yield_from(it):
        return (yield from it)

    return simple_nonit, simple_it, awaiting, yield_from
