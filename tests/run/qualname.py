# cython: binding=True
# mode: run
# tag: cyfunction,qualname

from __future__ import print_function

import cython
import sys


def test_qualname():
    """
    >>> test_qualname.__qualname__
    'test_qualname'
    >>> test_qualname.__qualname__ = 123 #doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: __qualname__ must be set to a ... object
    >>> test_qualname.__qualname__ = 'foo'
    >>> test_qualname.__qualname__
    'foo'
    """


def test_builtin_qualname():
    """
    >>> test_builtin_qualname()
    list.append
    len
    """
    if sys.version_info >= (3, 3):
        print([1, 2, 3].append.__qualname__)
        print(len.__qualname__)
    else:
        print('list.append')
        print('len')


def test_nested_qualname():
    """
    >>> outer, lambda_func, XYZ = test_nested_qualname()
    defining class XYZ XYZ qualname
    defining class Inner XYZ.Inner qualname

    >>> outer_result = outer()
    defining class Test test_nested_qualname.<locals>.outer.<locals>.Test qualname
    >>> outer_result.__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test'
    >>> outer_result.test.__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test.test'

    >>> outer_result().test.__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test.test'

    >>> outer_result_test_result = outer_result().test()
    defining class XYZInner XYZinner qualname
    >>> outer_result_test_result.__qualname__
    'XYZinner'
    >>> outer_result_test_result.Inner.__qualname__
    'XYZinner.Inner'
    >>> outer_result_test_result.Inner.inner.__qualname__
    'XYZinner.Inner.inner'

    >>> lambda_func.__qualname__
    'test_nested_qualname.<locals>.<lambda>'

    >>> XYZ.__qualname__
    'XYZ'
    >>> XYZ.Inner.__qualname__
    'XYZ.Inner'
    >>> XYZ.Inner.inner.__qualname__
    'XYZ.Inner.inner'
    """
    def outer():
        class Test(object):
            print("defining class Test", __qualname__, __module__)
            def test(self):
                global XYZinner
                class XYZinner:
                    print("defining class XYZInner", __qualname__, __module__)
                    class Inner:
                        def inner(self):
                            pass

                return XYZinner
        return Test

    global XYZ
    class XYZ(object):
        print("defining class XYZ", __qualname__, __module__)
        class Inner(object):
            print("defining class Inner", __qualname__, __module__)
            def inner(self):
                pass

    return outer, lambda:None, XYZ


@cython.cclass
class CdefClass:
    """
    >>> print(CdefClass.qn, CdefClass.m)
    CdefClass qualname
    >>> print(CdefClass.__qualname__, CdefClass.__module__)
    CdefClass qualname
    """
    qn = __qualname__
    m = __module__
