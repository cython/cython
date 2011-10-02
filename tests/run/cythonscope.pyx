cimport cython

from cython cimport _testscope as tester
from cython cimport TestClass, _testclass_new as TestClass_New
from cython cimport test_call, test_dep
from cython.view cimport _testscope as viewtester

from cpython cimport PyObject

cdef extern from *:
    # TestClass stuff
    cdef struct __pyx_TestClass_obj:
        int value

    # Type pointer
    cdef PyObject *TestClassType "__pyx_TestClass_type"

    # This is a cdef function
    cdef __pyx_TestClass_New(int)

    # These are methods and therefore have no prototypes
    cdef __pyx_TestClass_cdef_method(TestClass self, int value)
    cdef __pyx_TestClass_cpdef_method(TestClass self, int value, int skip_dispatch)
    cdef __pyx_TestClass_def_method(object self, object value)

    cdef __pyx_TestClass_cdef_cname(TestClass self, int value)
    cdef __pyx_TestClass_cpdef_cname(TestClass self, int value, int skip_dispatch)
    cdef __pyx_TestClass_def_cname(object self, object value)

    cdef __pyx_test_dep(object)
    cdef __pyx_test_call_other_cy_util(object)


def test_cdef_cython_utility():
    """
    >>> test_cdef_cython_utility()
    hello from cython scope, value=4
    hello from cython.view scope, value=4
    hello from cython scope, value=3
    hello from cython.view scope, value=3
    """
    print cython._testscope(4)
    print cython.view._testscope(4)
    print tester(3)
    print viewtester(3)

def test_cdef_class_cython_utility():
    """
    >>> test_cdef_class_cython_utility()
    7
    14
    TestClass(20)
    TestClass(50)
    """
    cdef __pyx_TestClass_obj *objstruct

    obj =  TestClass_New(7)
    objstruct = <__pyx_TestClass_obj *> obj
    print objstruct.value

    obj =  __pyx_TestClass_New(14)
    objstruct = <__pyx_TestClass_obj *> obj
    print objstruct.value

    print (<object> TestClassType)(20)
    print TestClass(50)

def test_extclass_c_methods():
    """
    >>> test_extclass_c_methods()
    Hello from cdef_method 1
    Hello from cpdef_method 2
    Hello from def_method 3
    Hello from cdef_cname_method 4
    Hello from cpdef_cname_method 5
    Hello from def_cname_method 6
    Hello from cdef_method 1
    Hello from cpdef_method 2
    Hello from def_method 3
    Hello from cdef_cname_method 4
    Hello from cpdef_cname_method 5
    Hello from def_cname_method 6
    """
    cdef TestClass obj1 = TestClass(11)
    cdef TestClass obj2 = TestClass_New(22)

    __pyx_TestClass_cdef_method(obj1, 1)
    __pyx_TestClass_cpdef_method(obj1, 2, True)
    __pyx_TestClass_def_method(obj1, 3)

    __pyx_TestClass_cdef_cname(obj1, 4)
    __pyx_TestClass_cpdef_cname(obj1, 5, True)
    __pyx_TestClass_def_cname(obj1, 6)

    __pyx_TestClass_cdef_method(obj2, 1)
    __pyx_TestClass_cpdef_method(obj2, 2, True)
    __pyx_TestClass_def_method(obj2, 3)

    __pyx_TestClass_cdef_cname(obj2, 4)
    __pyx_TestClass_cpdef_cname(obj2, 5, True)
    __pyx_TestClass_def_cname(obj2, 6)

def test_extclass_cython_methods():
    """
    >>> test_extclass_cython_methods()
    Hello from cdef_method 1
    Hello from cpdef_method 2
    Hello from def_method 3
    Hello from cdef_cname_method 4
    Hello from cpdef_cname_method 5
    Hello from def_cname_method 6
    Hello from cdef_method 1
    Hello from cpdef_method 2
    Hello from def_method 3
    Hello from cdef_cname_method 4
    Hello from cpdef_cname_method 5
    Hello from def_cname_method 6
    """
    cdef TestClass obj1 = TestClass(11)
    cdef TestClass obj2 = TestClass_New(22)

    obj1.cdef_method(1)
    obj1.cpdef_method(2)
    obj1.def_method(3)
    obj1.cdef_cname_method(4)
    obj1.cpdef_cname_method(5)
    obj1.def_cname_method(6)

    obj2.cdef_method(1)
    obj2.cpdef_method(2)
    obj2.def_method(3)
    obj2.cdef_cname_method(4)
    obj2.cpdef_cname_method(5)
    obj2.def_cname_method(6)

def test_cython_utility_dep():
    """
    >>> test_cython_utility_dep()
    test_dep first
    test_call
    test_dep second
    test_dep third
    test_call
    test_dep fourth
    """
    test_dep('first')
    test_call('second')
    __pyx_test_dep('third')
    __pyx_test_call_other_cy_util('fourth')

def viewobjs():
    """
    >>> viewobjs()
    <strided and direct or indirect>
    <strided and direct>
    <strided and indirect>
    <contiguous and direct>
    <contiguous and indirect>
    """
    print cython.view.generic
    print cython.view.strided
    print cython.view.indirect
    #print cython.view.generic_contiguous
    print cython.view.contiguous
    print cython.view.indirect_contiguous
