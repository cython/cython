# cython: language_level=3, binding=True
# mode: run
# tag: pep492, asyncfor, await


def run_async(coro):
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
    """

    async def simple():
        return 10

    async def awaiting(awaitable):
        return await awaitable

    return simple, awaiting
