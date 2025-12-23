# cython: binding=True
# mode: run
# tag: cyfunction, qualname, pure3.5

from __future__ import print_function

import cython


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
    print([1, 2, 3].append.__qualname__)
    print(len.__qualname__)


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

    #>>> print(CdefClass.l["__qualname__"], CdefClass.l["__module__"])
    #CdefClass qualname
    """
    qn = __qualname__
    m = __module__

    # TODO - locals and cdef classes is unreliable, irrespective of qualname
    # l = locals().copy()


# TODO - locals and cdef classes is unreliable, irrespective of qualname
#@cython.cclass
#class CdefOnlyLocals:
#    """
#    >>> print(CdefOnlyLocals.l["__qualname__"], CdefOnlyLocals.l["__module__"])
#    CdefOnlyLocals qualname
#    """
#    l = locals().copy()

@cython.cclass
class CdefModifyNames:
    """
    >>> print(CdefModifyNames.qn_reassigned, CdefModifyNames.m_reassigned)
    I'm not a qualname I'm not a module

    # TODO - enable when https://github.com/cython/cython/issues/4815 is fixed
    #>>> hasattr(CdefModifyNames, "qn_deleted")
    #False
    #>>> hasattr(CdefModifyNames, "m_deleted")
    #False

    #>>> print(CdefModifyNames.l["__qualname__"], CdefModifyNames.l["__module__"])
    #I'm not a qualname I'm not a module
    """
    __qualname__ = "I'm not a qualname"
    __module__ = "I'm not a module"
    qn_reassigned = __qualname__
    m_reassigned = __module__
    # TODO - locals and cdef classes is unreliable, irrespective of qualname
    #l = locals().copy()
    # TODO del inside cdef class scope is broken
    # https://github.com/cython/cython/issues/4815
    #del __qualname__
    #del __module__
    #try:
    #    qn_deleted = __qualname__
    #except NameError:
    #    pass
    #try:
    #    m_deleted = __module__
    #except NameError:
    #    pass
