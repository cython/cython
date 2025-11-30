# mode: run
# tag: generators, gh3265

cdef extern from *:
    int CYTHON_COMPILING_IN_LIMITED_API

try:
    import backports_abc
except ImportError: pass
else: backports_abc.patch()

try:
    from collections.abc import Generator
except ImportError:
    try:
        from collections import Generator
    except ImportError:
        Generator = object  # easy win


def skip_in_limited_api(f):
    if not CYTHON_COMPILING_IN_LIMITED_API:
        return f


def very_simple():
    """
    >>> x = very_simple()
    >>> next(x)
    1
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    >>> next(x)
    Traceback (most recent call last):
    StopIteration

    >>> x = very_simple()
    >>> x.send(1)
    Traceback (most recent call last):
    TypeError: can't send non-None value to a just-started generator
    """
    yield 1


def attributes():
    """
    >>> x = attributes()
    >>> x.__name__
    'attributes'
    >>> x.__qualname__
    'attributes'
    >>> x.gi_running  # before next()
    False
    >>> inner = next(x)
    >>> x.gi_running  # after next()
    False
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    >>> x.gi_running  # after termination
    False

    >>> y = inner()
    >>> y.__name__
    '<lambda>'
    >>> y.__qualname__
    'attributes.<locals>.inner.<locals>.<lambda>'

    >>> y.__name__ = 123
    Traceback (most recent call last):
    TypeError: __name__ must be set to a string object
    >>> y.__name__
    '<lambda>'
    >>> y.__qualname__ = None
    Traceback (most recent call last):
    TypeError: __qualname__ must be set to a string object
    >>> y.__qualname__
    'attributes.<locals>.inner.<locals>.<lambda>'

    >>> y.__name__ = 'abc'
    >>> y.__name__
    'abc'
    >>> y.__name__ = None
    Traceback (most recent call last):
    TypeError: __name__ must be set to a string object
    >>> y.__name__
    'abc'
    >>> y.__qualname__ = 'huhu'
    >>> y.__qualname__
    'huhu'
    >>> y.__qualname__ = 123
    Traceback (most recent call last):
    TypeError: __qualname__ must be set to a string object
    >>> y.__qualname__
    'huhu'
    """
    def inner():
        return (lambda : (yield 1))
    yield inner()


def simple():
    """
    >>> x = simple()
    >>> list(x)
    [1, 2, 3]
    """
    yield 1
    yield 2
    yield 3

def simple_seq(seq):
    """
    >>> x = simple_seq("abc")
    >>> list(x)
    ['a', 'b', 'c']
    """
    for i in seq:
        yield i

def simple_send():
    """
    >>> x = simple_send()
    >>> next(x)
    >>> x.send(1)
    1
    >>> x.send(2)
    2
    >>> x.send(3)
    3
    """
    i = None
    while True:
        i = yield i

def raising():
    """
    >>> x = raising()
    >>> next(x)
    Traceback (most recent call last):
    KeyError: 'foo'
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    """
    yield {}['foo']

def with_outer(*args):
    """
    >>> x = with_outer(1, 2, 3)
    >>> list(x())
    [1, 2, 3]
    """
    def generator():
        for i in args:
            yield i
    return generator

def with_outer_raising(*args):
    """
    >>> x = with_outer_raising(1, 2, 3)
    >>> list(x())
    [1, 2, 3]
    """
    def generator():
        for i in args:
            yield i
        raise StopIteration
    return generator

def test_close():
    """
    >>> x = test_close()
    >>> x.close()
    >>> x = test_close()
    >>> next(x)
    >>> x.close()
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    """
    while True:
        yield

def test_ignore_close():
    """
    >>> x = test_ignore_close()
    >>> x.close()
    >>> x = test_ignore_close()
    >>> next(x)
    >>> x.close()
    Traceback (most recent call last):
    RuntimeError: generator ignored GeneratorExit
    """
    try:
        yield
    except GeneratorExit:
        yield

def check_throw():
    """
    >>> x = check_throw()
    >>> x.throw(ValueError)
    Traceback (most recent call last):
    ValueError
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    >>> x = check_throw()
    >>> next(x)
    >>> x.throw(ValueError)
    >>> next(x)
    >>> x.throw(IndexError, "oops")
    Traceback (most recent call last):
    IndexError: oops
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    """
    while True:
        try:
            yield
        except ValueError:
            pass

def test_first_assignment():
    """
    >>> gen = test_first_assignment()
    >>> next(gen)
    5
    >>> next(gen)
    10
    >>> next(gen)
    (5, 10)
    """
    cdef x = 5 # first
    yield x
    cdef y = 10 # first
    yield y
    yield (x,y)

def test_swap_assignment():
    """
    >>> gen = test_swap_assignment()
    >>> next(gen)
    (5, 10)
    >>> next(gen)
    (10, 5)
    """
    x,y = 5,10
    yield (x,y)
    x,y = y,x   # no ref-counting here
    yield (x,y)


class Foo(object):
    """
    >>> obj = Foo()
    >>> list(obj.simple(1, 2, 3))
    [1, 2, 3]
    """
    def simple(self, *args):
        for i in args:
            yield i

def generator_nonlocal():
    """
    >>> g = generator_nonlocal()
    >>> list(g(5))
    [2, 3, 4, 5, 6]
    """
    def f(x):
        def g(y):
            nonlocal x
            for i in range(y):
                x += 1
                yield x
        return g
    return f(1)

def test_nested(a, b, c):
    """
    >>> obj = test_nested(1, 2, 3)
    >>> [i() for i in obj]
    [1, 2, 3, 4]
    """
    def one():
        return a
    def two():
        return b
    def three():
        return c
    def new_closure(a, b):
        def sum():
            return a + b
        return sum
    yield one
    yield two
    yield three
    yield new_closure(a, c)


def tolist(func):
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))
    return wrapper

@tolist
def test_decorated(*args):
    """
    >>> test_decorated(1, 2, 3)
    [1, 2, 3]
    """
    for i in args:
        yield i


def test_return(a):
    """
    >>> d = dict()
    >>> obj = test_return(d)
    >>> next(obj)
    1
    >>> next(obj)
    Traceback (most recent call last):
    StopIteration
    >>> d['i_was_here']
    True
    """
    yield 1
    a['i_was_here'] = True
    return


def test_return_in_finally(a):
    """
    >>> d = dict()
    >>> obj = test_return_in_finally(d)
    >>> next(obj)
    1
    >>> next(obj)
    Traceback (most recent call last):
    StopIteration
    >>> d['i_was_here']
    True

    >>> d = dict()
    >>> obj = test_return_in_finally(d)
    >>> next(obj)
    1
    >>> obj.send(2)
    Traceback (most recent call last):
    StopIteration
    >>> d['i_was_here']
    True

    >>> obj = test_return_in_finally(None)
    >>> next(obj)
    1
    >>> next(obj)
    Traceback (most recent call last):
    StopIteration

    >>> obj = test_return_in_finally(None)
    >>> next(obj)
    1
    >>> obj.send(2)
    Traceback (most recent call last):
    StopIteration
    """
    yield 1
    try:
        a['i_was_here'] = True
    finally:
        return


def test_return_none_in_finally(a):
    """
    >>> d = dict()
    >>> obj = test_return_none_in_finally(d)
    >>> next(obj)
    1
    >>> next(obj)
    Traceback (most recent call last):
    StopIteration
    >>> d['i_was_here']
    True

    >>> obj = test_return_none_in_finally(None)
    >>> next(obj)
    1
    >>> next(obj)
    Traceback (most recent call last):
    StopIteration
    """
    yield 1
    try:
        a['i_was_here'] = True
    finally:
        return None


def test_copied_yield(foo):
    """
    >>> class Manager(object):
    ...    def __enter__(self):
    ...        return self
    ...    def __exit__(self, type, value, tb):
    ...        pass
    >>> list(test_copied_yield(Manager()))
    [1]
    """
    with foo:
        yield 1

def test_nested_yield():
    """
    >>> obj = test_nested_yield()
    >>> next(obj)
    1
    >>> obj.send(2)
    2
    >>> obj.send(3)
    3
    >>> obj.send(4)
    Traceback (most recent call last):
    StopIteration
    """
    yield (yield (yield 1))

def test_inside_lambda():
    """
    >>> obj = test_inside_lambda()()
    >>> next(obj)
    1
    >>> next(obj)
    2
    >>> next(obj)
    Traceback (most recent call last):
    StopIteration
    """
    return lambda:((yield 1), (yield 2))

def test_nested_gen(int n):
    """
    >>> [list(a) for a in test_nested_gen(5)]
    [[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]
    """
    for a in range(n):
        yield (b for b in range(a))

def test_lambda(n):
    """
    >>> [i() for i in test_lambda(3)]
    [0, 1, 2]
    """
    for i in range(n):
        yield lambda : i


def test_with_gil_section():
    """
    >>> list(test_with_gil_section())
    [0, 1, 2]
    """
    cdef int i
    with nogil:
        for i in range(3):
            with gil:
                yield i


def test_double_with_gil_section():
    """
    >>> list(test_double_with_gil_section())
    [0, 1, 2, 3]
    """
    cdef int i,j
    with nogil:
        for i in range(2):
            with gil:
                with nogil:
                    for j in range(2):
                        with gil:
                            yield i*2+j
                with nogil:
                    pass
            with gil:
                pass


def test_generator_abc():
    """
    >>> isinstance(test_generator_abc(), Generator)
    True

    >>> try:
    ...     from collections.abc import Generator
    ... except ImportError:
    ...     try:
    ...         from collections import Generator
    ...     except ImportError:
    ...         Generator = object  # easy win

    >>> isinstance(test_generator_abc(), Generator)
    True
    >>> isinstance((lambda:(yield))(), Generator)
    True
    """
    yield 1


# No good solution for generating frame objects in Limited API
@skip_in_limited_api
def test_generator_frame(a=1):
    """
    >>> gen = test_generator_frame()
    >>> import types
    >>> isinstance(gen.gi_frame, types.FrameType) or gen.gi_frame
    True
    >>> gen.gi_frame is gen.gi_frame  # assert that it's cached
    True
    >>> gen.gi_frame.f_code is not None
    True
    >>> code_obj = gen.gi_frame.f_code
    >>> code_obj.co_argcount
    1
    >>> code_obj.co_varnames
    ('a', 'b')
    """
    b = a + 1
    yield b


# GH Issue 3265 - **kwds could cause a crash in some cases due to not
# handling NULL pointers (in testing it shows as a REFNANNY error).
# This was on creation of the generator and
# doesn't really require it to be iterated through:

def some_function():
    return 0


def test_generator_kwds1(**kwargs):
    """
    >>> for a in test_generator_kwds1():
    ...     print(a)
    0
    """
    yield some_function(**kwargs)


def test_generator_kwds2(**kwargs):
    """
    >>> for a in test_generator_kwds2():
    ...     print(a)
    0
    """
    yield 0


def test_generator_kwds3(**kwargs):
    """
    This didn't actually crash before but is still worth a try
    >>> len(list(test_generator_kwds3()))
    0
    >>> for a in test_generator_kwds3(a=1):
    ...    print(a)
    a
    """
    yield from kwargs.keys()


@skip_in_limited_api
def test_generator_frame(a=1):
    """
    >>> gen = test_generator_frame()
    >>> import types
    >>> isinstance(gen.gi_frame, types.FrameType) or gen.gi_frame
    True
    >>> gen.gi_frame is gen.gi_frame  # assert that it's cached
    True
    >>> gen.gi_frame.f_code is not None
    True
    >>> code_obj = gen.gi_frame.f_code
    >>> code_obj.co_argcount
    1
    >>> code_obj.co_varnames
    ('a', 'b')
    """
    b = a + 1
    yield b
