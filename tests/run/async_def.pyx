# cython: language_level=3, binding=True
# mode: run
# tag: pep492, await, gh3337, gh2273

"""
Cython specific tests in addition to "test_coroutines_pep492.pyx"
(which is copied from CPython).
"""

import asyncio
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

# Test iscoroutinefunction()
def func_def_example():
    return 1

def func_gen_example():
    yield 1

async def func_async_def_example():
    return 1

async def func_async_gen_example():
    yield 1

class ExampleClass:
    async def method_async_def_example(self):
        return 1

    async def method_async_gen_example(self):
        yield 1

example_obj = ExampleClass()


def test_asyncio_iscoroutinefunction_gh2273(func):
    """
    >>> test_asyncio_iscoroutinefunction_gh2273(func_def_example)
    False
    >>> test_asyncio_iscoroutinefunction_gh2273(func_gen_example)
    False
    >>> test_asyncio_iscoroutinefunction_gh2273(func_async_def_example)
    True
    >>> test_asyncio_iscoroutinefunction_gh2273(func_async_gen_example)
    True
    >>> test_asyncio_iscoroutinefunction_gh2273(ExampleClass.method_async_def_example)
    True
    >>> test_asyncio_iscoroutinefunction_gh2273(ExampleClass.method_async_gen_example)
    True
    >>> test_asyncio_iscoroutinefunction_gh2273(example_obj.method_async_def_example)
    True
    >>> test_asyncio_iscoroutinefunction_gh2273(example_obj.method_async_gen_example)
    True
    """
    return asyncio.iscoroutinefunction(func)
