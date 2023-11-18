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
