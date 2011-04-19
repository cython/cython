# mode: run
# tag: generators

try:
    from builtins import next # Py3k
except ImportError:
    def next(it):
        return it.next()

if hasattr(__builtins__, 'GeneratorExit'):
    GeneratorExit = __builtins__.GeneratorExit
else: # < 2.5
    GeneratorExit = StopIteration

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
