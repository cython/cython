# mode: run
# distutils: define_macros = CYTHON_TRACE=1 CYTHON_PROFILE=1

"""
Global compiler flags do not enable instrumentation of an untraced module.

>>> list(generator())
[1, 2]
>>> coro = coroutine()
>>> coro.send(None)
Traceback (most recent call last):
...
StopIteration: 3
>>> agen = async_generator()
>>> agen.__anext__().send(None)
Traceback (most recent call last):
...
StopIteration: 4
>>> agen.__anext__().send(None)
Traceback (most recent call last):
...
StopAsyncIteration
"""


def generator():
    yield 1
    yield 2


async def coroutine():
    return 3


async def async_generator():
    yield 4
