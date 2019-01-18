# cython: language_level=3
# mode: run
# tag: pep492, pure3.5


async def test_coroutine_frame(awaitable):
    """
    >>> class Awaitable(object):
    ...     def __await__(self):
    ...         return iter([2])

    >>> coro = test_coroutine_frame(Awaitable())
    >>> import types
    >>> isinstance(coro.cr_frame, types.FrameType) or coro.cr_frame
    True
    >>> coro.cr_frame is coro.cr_frame  # assert that it's cached
    True
    >>> coro.cr_frame.f_code is not None
    True
    >>> code_obj = coro.cr_frame.f_code
    >>> code_obj.co_argcount
    1
    >>> code_obj.co_varnames
    ('awaitable', 'b')

    >>> next(coro.__await__())  # avoid "not awaited" warning
    2
    """
    b = await awaitable
    return b
