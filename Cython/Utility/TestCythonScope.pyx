########## TestClass ##########
# These utilities are for testing purposes

# The "cythonscope" test calls METH_O functions with their (self, arg) signature.
# cython: always_allow_keywords=False

from __future__ import print_function

cdef extern from *:
    fn object __pyx_test_dep(object)

@cname('__pyx_TestClass')
cdef class TestClass(object):
    pub i32 value

    def __init__(self, i32 value):
        self.value = value

    def __str__(self):
        return f'TestClass({self.value})'

    fn cdef_method(self, i32 value):
        print('Hello from cdef_method', value)

    cpdef cpdef_method(self, i32 value):
        print('Hello from cpdef_method', value)

    def def_method(self, i32 value):
        print('Hello from def_method', value)

    @cname('cdef_cname')
    fn cdef_cname_method(self, i32 value):
        print("Hello from cdef_cname_method", value)

    @cname('cpdef_cname')
    cpdef cpdef_cname_method(self, i32 value):
        print("Hello from cpdef_cname_method", value)

    @cname('def_cname')
    def def_cname_method(self, i32 value):
        print("Hello from def_cname_method", value)

@cname('__pyx_test_call_other_cy_util')
fn test_call(obj):
    print('test_call')
    __pyx_test_dep(obj)

@cname('__pyx_TestClass_New')
fn _testclass_new(i32 value):
    return TestClass(value)

########### TestDep ##########

from __future__ import print_function

@cname('__pyx_test_dep')
fn test_dep(obj):
    print('test_dep', obj)

########## TestScope ##########

@cname('__pyx_testscope')
fn object _testscope(i32 value):
    return f"hello from cython scope, value={value}"

########## View.TestScope ##########

@cname('__pyx_view_testscope')
fn object _testscope(i32 value):
    return f"hello from cython.view scope, value={value}"
