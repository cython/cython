# mode: run

from __future__ import with_statement

def typename(t):
    name = type(t).__name__
    return u"<type '%s'>" % name

class MyException(Exception):
    pass

class ContextManager(object):
    def __init__(self, value, exit_ret = None):
        self.value = value
        self.exit_ret = exit_ret

    def __exit__(self, a, b, tb):
        print u"exit", typename(a), typename(b), typename(tb)
        return self.exit_ret

    def __enter__(self):
        print u"enter"
        return self.value

def no_as():
    """
    >>> no_as()
    enter
    hello
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager(u"value"):
        print u"hello"

def basic():
    """
    >>> basic()
    enter
    value
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager(u"value") as x:
        print x

def with_pass():
    """
    >>> with_pass()
    enter
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager(u"value") as x:
        pass

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
        with ContextManager(u"value", exit_ret=exit_ret) as value:
            print value
            raise MyException()
    except:
        print u"outer except"

def multitarget():
    """
    >>> multitarget()
    enter
    1 2 3 4 5
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager((1, 2, (3, (4, 5)))) as (a, b, (c, (d, e))):
        print a, b, c, d, e

def tupletarget():
    """
    >>> tupletarget()
    enter
    (1, 2, (3, (4, 5)))
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    with ContextManager((1, 2, (3, (4, 5)))) as t:
        print t

def typed():
    """
    >>> typed()
    enter
    10
    exit <type 'NoneType'> <type 'NoneType'> <type 'NoneType'>
    """
    cdef unsigned char i
    c = ContextManager(255)
    with c as i:
        i += 11
        print i

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
    with ContextManager(1), ContextManager(2) as x, ContextManager(u'value') as y,\
            ContextManager(3), ContextManager((1, 2, (3, (4, 5)))) as (a, b, (c, (d, e))):
        with ContextManager(u'nested') as nested:
            print x
            print y
            print a, b, c, d, e
            print nested

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
            self.assertEqual(1, a1)
            self.assertEqual(2, a2)
            self.assertEqual(10, b1)
            self.assertEqual(20, b2)
