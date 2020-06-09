# cython: language_level=3, binding=True
# mode: run
# tag: pep492, await, gh3337

"""
Cython specific tests in addition to "test_coroutines_pep492.pyx"
(which is copied from CPython).
"""

import sys


def run_async(coro):
    #assert coro.__class__ is types.GeneratorType
    assert coro.__class__.__name__ in ('coroutine', '_GeneratorWrapper'), coro.__class__.__name__

    buffer = []
    result = None
    while True:
        try:
            buffer.append(coro.send(None))
        except StopIteration as ex:
            result = ex.value if sys.version_info >= (3, 5) else ex.args[0] if ex.args else None
            break
    return buffer, result


async def test_async_temp_gh3337(x, y):
    """
    >>> run_async(test_async_temp_gh3337(2, 3))
    ([], -1)
    >>> run_async(test_async_temp_gh3337(3, 2))
    ([], 0)
    """
    return min(x - y, 0)
