import sys

def typename(t):
    name = type(t).__name__
    if sys.version_info < (2,5):
        if name == 'classobj' and issubclass(t, MyException):
            name = 'type'
        elif name == 'instance' and isinstance(t, MyException):
            name = 'MyException'
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

def multimanager():
    """
    >>> multimanager()
    enter
    enter
    enter
    enter
    enter
    enter
    2
    value
    1 2 3 4 5
    nested
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager(1), ContextManager(2) as x, ContextManager('value') as y,\
            ContextManager(3), ContextManager((1, 2, (3, (4, 5)))) as (a, b, (c, (d, e))):
        with ContextManager('nested') as nested:
            print(x)
            print(y)
            print('%s %s %s %s %s' % (a, b, c, d, e))
            print(nested)

# Tests borrowed from pyregr test_with.py,
# modified to follow the constraints of Cython.
import unittest

class Dummy(object):
    def __init__(self, value=None, gobble=False):
        if value is None:
            value = self
        self.value = value
        self.gobble = gobble
        self.enter_called = False
        self.exit_called = False

    def __enter__(self):
        self.enter_called = True
        return self.value

    def __exit__(self, *exc_info):
        self.exit_called = True
        self.exc_info = exc_info
        if self.gobble:
            return True

class InitRaises(object):
    def __init__(self): raise RuntimeError()

class EnterRaises(object):
    def __enter__(self): raise RuntimeError()
    def __exit__(self, *exc_info): pass

class ExitRaises(object):
    def __enter__(self): pass
    def __exit__(self, *exc_info): raise RuntimeError()

class NestedWith(unittest.TestCase):
    """
    >>> NestedWith().runTest()
    """

    def runTest(self):
        self.testNoExceptions()
        self.testExceptionInExprList()
        self.testExceptionInEnter()
        self.testExceptionInExit()
        self.testEnterReturnsTuple()

    def testNoExceptions(self):
        with Dummy() as a, Dummy() as b:
            self.assertTrue(a.enter_called)
            self.assertTrue(b.enter_called)
        self.assertTrue(a.exit_called)
        self.assertTrue(b.exit_called)

    def testExceptionInExprList(self):
        try:
            with Dummy() as a, InitRaises():
                pass
        except:
            pass
        self.assertTrue(a.enter_called)
        self.assertTrue(a.exit_called)

    def testExceptionInEnter(self):
        try:
            with Dummy() as a, EnterRaises():
                self.fail('body of bad with executed')
        except RuntimeError:
            pass
        else:
            self.fail('RuntimeError not reraised')
        self.assertTrue(a.enter_called)
        self.assertTrue(a.exit_called)

    def testExceptionInExit(self):
        body_executed = False
        with Dummy(gobble=True) as a, ExitRaises():
            body_executed = True
        self.assertTrue(a.enter_called)
        self.assertTrue(a.exit_called)
        self.assertTrue(body_executed)
        self.assertNotEqual(a.exc_info[0], None)

    def testEnterReturnsTuple(self):
        with Dummy(value=(1,2)) as (a1, a2), \
             Dummy(value=(10, 20)) as (b1, b2):
            self.assertEquals(1, a1)
            self.assertEquals(2, a2)
            self.assertEquals(10, b1)
            self.assertEquals(20, b2)
