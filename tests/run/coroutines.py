# cython: language_level=3
# mode: run
# tag: pep492, pure3.5, gh1462, async, await

import cython

def skip_in_limited_api(f):
    # CYTHON_COMPILING_IN_LIMITED_API is cdef extern in pxd file
    if not cython.compiled or not CYTHON_COMPILING_IN_LIMITED_API:
        return f

# Limited API isn't able to return useful frames for coroutines
@skip_in_limited_api
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


# gh1462: Using decorators on coroutines.

def pass_through(func):
    return func


@pass_through
async def test_pass_through():
    """
    >>> t = test_pass_through()
    >>> try: t.send(None)
    ... except StopIteration as ex:
    ...     print(ex.args[0] if ex.args else None)
    ... else: print("NOT STOPPED!")
    None
    """


@pass_through(pass_through)
async def test_pass_through_with_args():
    """
    >>> t = test_pass_through_with_args()
    >>> try: t.send(None)
    ... except StopIteration as ex:
    ...     print(ex.args[0] if ex.args else None)
    ... else: print("NOT STOPPED!")
    None
    """
