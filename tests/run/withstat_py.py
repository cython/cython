# mode: run

def typename(t):
    name = type(t).__name__
    return "<type '%s'>" % name


class MyException(Exception):
    pass


class ContextManager(object):
    def __init__(self, value, exit_ret = None):
        self.value = value
        self.exit_ret = exit_ret

    def __exit__(self, a, b, tb):
        print("exit %s %s %s" % (typename(a), typename(b), typename(tb)))
        return self.exit_ret

    def __enter__(self):
        print("enter")
        return self.value


def no_as():
    """
    >>> no_as()
    enter
    hello
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager("value"):
        print("hello")


def basic():
    """
    >>> basic()
    enter
    value
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager("value") as x:
        print(x)


def with_pass():
    """
    >>> with_pass()
    enter
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager("value") as x:
        pass


def with_return():
    """
    >>> print(with_return())
    enter
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    value
    """
    with ContextManager("value") as x:
        return x


def with_break():
    """
    >>> print(with_break())
    enter
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    a
    """
    for c in list("abc"):
        with ContextManager("value") as x:
            break
        print("FAILED")
    return c


def with_continue():
    """
    >>> print(with_continue())
    enter
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    enter
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    enter
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    c
    """
    for c in list("abc"):
        with ContextManager("value") as x:
            continue
        print("FAILED")
    return c


def with_exception(exit_ret):
    """
    >>> with_exception(None)
    enter
    value
    exit <type 'type'> <type 'MyException'> <type 'traceback'>
    outer except
    >>> with_exception(True)
    enter
    value
    exit <type 'type'> <type 'MyException'> <type 'traceback'>
    """
    try:
        with ContextManager("value", exit_ret=exit_ret) as value:
            print(value)
            raise MyException()
    except:
        print("outer except")


def with_real_lock():
    """
    >>> with_real_lock()
    about to acquire lock
    holding lock
    lock no longer held
    """
    from threading import Lock
    lock = Lock()

    print("about to acquire lock")

    with lock:
        print("holding lock")

    print("lock no longer held")


def functions_in_with():
    """
    >>> f = functions_in_with()
    enter
    exit <type 'type'> <type 'MyException'> <type 'traceback'>
    outer except
    >>> f(1)[0]
    1
    >>> print(f(1)[1])
    value
    """
    try:
        with ContextManager("value") as value:
            def f(x): return x, value
            make = lambda x:x()
            raise make(MyException)
    except:
        print("outer except")
    return f


def multitarget():
    """
    >>> multitarget()
    enter
    1 2 3 4 5
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager((1, 2, (3, (4, 5)))) as (a, b, (c, (d, e))):
        print('%s %s %s %s %s' % (a, b, c, d, e))


def tupletarget():
    """
    >>> tupletarget()
    enter
    (1, 2, (3, (4, 5)))
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager((1, 2, (3, (4, 5)))) as t:
        print(t)


class GetManager(object):
    def get(self, *args):
        return ContextManager(*args)


def manager_from_expression():
    """
    >>> manager_from_expression()
    enter
    1
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    enter
    2
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with GetManager().get(1) as x:
        print(x)
    g = GetManager()
    with g.get(2) as x:
        print(x)

def manager_from_ternary(use_first):
    """
    >>> manager_from_ternary(True)
    enter
    exit <type 'type'> <type 'ValueError'> <type 'traceback'>
    >>> manager_from_ternary(False)
    enter
    exit <type 'type'> <type 'ValueError'> <type 'traceback'>
    In except
    """
    # This is mostly testing a parsing problem, hence the
    # result of the ternary must be callable
    cm1_getter = lambda: ContextManager("1", exit_ret=True)
    cm2_getter = lambda: ContextManager("2")
    try:
        with (cm1_getter if use_first else cm2_getter)():
            raise ValueError
    except ValueError:
        print("In except")
