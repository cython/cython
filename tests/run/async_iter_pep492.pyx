# mode: run
# tag: pep492, asyncfor, await

import sys

if sys.version_info >= (3, 5, 0, 'beta'):
    # pass Cython implemented AsyncIter() into a Python async-for loop
    __doc__ = u"""
>>> def test_py35(AsyncIterClass):
...     buffer = []
...     async def coro():
...         async for i1, i2 in AsyncIterClass(1):
...             buffer.append(i1 + i2)
...     return coro, buffer

>>> testfunc, buffer = test_py35(AsyncIterOld if sys.version_info < (3, 5, 2) else AsyncIter)
>>> buffer
[]

>>> yielded, _ = run_async(testfunc(), check_type=False)
>>> yielded == [i * 100 for i in range(1, 11)] or yielded
True
>>> buffer == [i*2 for i in range(1, 101)] or buffer
True
"""


cdef class AsyncYieldFrom:
    cdef object obj
    def __init__(self, obj):
        self.obj = obj

    def __await__(self):
        yield from self.obj


cdef class AsyncYield:
    cdef object value
    def __init__(self, value):
        self.value = value

    def __await__(self):
        yield self.value


def run_async(coro, check_type='coroutine'):
    if check_type:
        assert coro.__class__.__name__ == check_type, \
            'type(%s) != %s' % (coro.__class__, check_type)

    buffer = []
    result = None
    while True:
        try:
            buffer.append(coro.send(None))
        except StopIteration as ex:
            result = ex.args[0] if ex.args else None
            break
    return buffer, result


cdef class AsyncIter:
    cdef long i
    cdef long aiter_calls
    cdef long max_iter_calls

    def __init__(self, long max_iter_calls=1):
        self.i = 0
        self.aiter_calls = 0
        self.max_iter_calls = max_iter_calls

    def __aiter__(self):
        self.aiter_calls += 1
        return self

    async def __anext__(self):
        self.i += 1
        assert self.aiter_calls <= self.max_iter_calls

        if not (self.i % 10):
            await AsyncYield(self.i * 10)

        if self.i > 100:
            raise StopAsyncIteration

        return self.i, self.i


cdef class AsyncIterOld(AsyncIter):
    """
    Same as AsyncIter, but with the old async-def interface for __aiter__().
    """
    async def __aiter__(self):
        self.aiter_calls += 1
        return self


def test_for_1():
    """
    >>> testfunc, buffer = test_for_1()
    >>> buffer
    []
    >>> yielded, _ = run_async(testfunc())
    >>> yielded == [i * 100 for i in range(1, 11)] or yielded
    True
    >>> buffer == [i*2 for i in range(1, 101)] or buffer
    True
    """
    buffer = []
    async def test1():
        async for i1, i2 in AsyncIter(1):
            buffer.append(i1 + i2)
    return test1, buffer


def test_for_2():
    """
    >>> testfunc, buffer = test_for_2()
    >>> buffer
    []
    >>> yielded, _ = run_async(testfunc())
    >>> yielded == [100, 200] or yielded
    True
    >>> buffer == [i for i in range(1, 21)] + ['end'] or buffer
    True
    """
    buffer = []
    async def test2():
        nonlocal buffer
        async for i in AsyncIter(2):
            buffer.append(i[0])
            if i[0] == 20:
                break
        else:
            buffer.append('what?')
        buffer.append('end')
    return test2, buffer



def test_for_3():
    """
    >>> testfunc, buffer = test_for_3()
    >>> buffer
    []
    >>> yielded, _ = run_async(testfunc())
    >>> yielded == [i * 100 for i in range(1, 11)] or yielded
    True
    >>> buffer == [i for i in range(1, 21)] + ['what?', 'end'] or buffer
    True
    """
    buffer = []
    async def test3():
        nonlocal buffer
        async for i in AsyncIter(3):
            if i[0] > 20:
                continue
            buffer.append(i[0])
        else:
            buffer.append('what?')
        buffer.append('end')
    return test3, buffer


cdef class NonAwaitableFromAnext:
    def __aiter__(self):
        return self

    def __anext__(self):
        return 123


def test_broken_anext():
    """
    >>> testfunc = test_broken_anext()
    >>> try: run_async(testfunc())
    ... except TypeError as exc:
    ...     assert ' int' in str(exc)
    ... else:
    ...     print("NOT RAISED!")
    """
    async def foo():
        async for i in NonAwaitableFromAnext():
            print('never going to happen')
    return foo


cdef class Manager:
    cdef readonly list counter
    def __init__(self, counter):
        self.counter = counter

    async def __aenter__(self):
        self.counter[0] += 10000

    async def __aexit__(self, *args):
        self.counter[0] += 100000


cdef class Iterable:
    cdef long i
    def __init__(self):
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i > 10:
            raise StopAsyncIteration
        self.i += 1
        return self.i


def test_with_for():
    """
    >>> test_with_for()
    111011
    333033
    20555255
    """
    I = [0]

    manager = Manager(I)
    iterable = Iterable()
    mrefs_before = sys.getrefcount(manager)
    irefs_before = sys.getrefcount(iterable)

    async def main():
        async with manager:
            async for i in iterable:
                I[0] += 1
        I[0] += 1000

    run_async(main())
    print(I[0])

    assert sys.getrefcount(manager) == mrefs_before
    assert sys.getrefcount(iterable) == irefs_before

    ##############

    async def main():
        nonlocal I

        async with Manager(I):
            async for i in Iterable():
                I[0] += 1
        I[0] += 1000

        async with Manager(I):
            async for i in Iterable():
                I[0] += 1
        I[0] += 1000

    run_async(main())
    print(I[0])

    ##############

    async def main():
        async with Manager(I):
            I[0] += 100
            async for i in Iterable():
                I[0] += 1
            else:
                I[0] += 10000000
        I[0] += 1000

        async with Manager(I):
            I[0] += 100
            async for i in Iterable():
                I[0] += 1
            else:
                I[0] += 10000000
        I[0] += 1000

    run_async(main())
    print(I[0])


# old-style pre-3.5.2 AIter protocol - no longer supported
#cdef class AI_old:
#    async def __aiter__(self):
#        1/0


cdef class AI_new:
    def __aiter__(self):
        1/0


def test_aiter_raises(AI):
    """
    #>>> test_aiter_raises(AI_old)
    #RAISED
    #0
    >>> test_aiter_raises(AI_new)
    RAISED
    0
    """
    CNT = 0

    async def foo():
        nonlocal CNT
        async for i in AI():
            CNT += 1
        CNT += 10

    try:
        run_async(foo())
    except ZeroDivisionError:
        print("RAISED")
    else:
        print("NOT RAISED")
    return CNT
