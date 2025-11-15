# cython: language_level=3str, binding=True
# mode: run
# tag: pep492, await, gh3337

"""
Cython specific tests in addition to "test_coroutines_pep492.pyx"
(which is copied from CPython).
"""


def run_async(coro, assert_type=True, send_value=None):
    if assert_type:
        #assert coro.__class__ is types.GeneratorType
        assert coro.__class__.__name__ in ('coroutine', '_GeneratorWrapper'), coro.__class__.__name__

    buffer = []
    result = None
    while True:
        try:
            buffer.append(coro.send(send_value))
        except StopIteration as ex:
            result = ex.value
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


async def outer_with_nested(called):
    """
    >>> called = []
    >>> _, inner = run_async(outer_with_nested(called))
    >>> called  # after outer_with_nested()
    ['outer', 'make inner', 'deco', 'return inner']
    >>> _ = run_async(inner())
    >>> called  # after inner()
    ['outer', 'make inner', 'deco', 'return inner', 'inner']
    """
    called.append('outer')

    def deco(f):
        called.append('deco')
        return f

    called.append('make inner')

    @deco
    async def inner():
        called.append('inner')
        return 1

    called.append('return inner')
    return inner

# used in "await_in_genexpr_iterator"
async def h(arg):
    return [arg, arg+1]

async def await_in_genexpr_iterator():
    """
    >>> _, x = run_async(await_in_genexpr_iterator())
    >>> x
    [4, 6]
    """
    lst = list  # obfuscate from any optimizations cython might try
    return lst(x*2 for x in await h(2))

def yield_in_genexpr_iterator():
    """
    Same test as await_in_genexpr_iterator but with yield.
    (Possibly in the wrong place, but grouped with related tests)

    >>> g = yield_in_genexpr_iterator()
    >>> g.send(None)
    >>> _, x = run_async(g, assert_type=False, send_value=[2, 3])
    >>> x
    [4, 6]
    """
    lst = list  # obfuscate from any optimizations cython might try
    return lst(x*2 for x in (yield))

def h_yield_from(arg):
    yield
    return [arg, arg+1]

def yield_from_in_genexpr_iterator():
    """
    Same test as await_in_genexpr_iterator but with "yield from".
    (Possibly in the wrong place, but grouped with related tests)

    >>> _, x = run_async(yield_from_in_genexpr_iterator(), assert_type=False)
    >>> x
    [4, 6]
    """
    lst = list  # obfuscate from any optimizations cython might try
    return lst(x*2 for x in (yield from h_yield_from(2)))

def test_is_running():
    """
    >>> co = test_is_running()
    >>> co.cr_running
    False
    >>> _, result = run_async(co, assert_type=False)
    >>> result
    True
    """
    async def inner():
        return inner_instance.cr_running

    inner_instance = inner()
    return inner_instance

def test_gen_is_running():
    """
    Generator test, here for convenience
    >>> gen = test_gen_is_running()
    >>> gen.gi_running
    False
    >>> tuple(gen)
    (True,)
    """

    def inner():
        yield inner_instance.gi_running

    inner_instance = inner()
    return inner_instance
