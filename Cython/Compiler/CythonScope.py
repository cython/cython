from Symtab import ModuleScope
from PyrexTypes import *
from UtilityCode import CythonUtilityCode
from Errors import error
from Scanning import StringSourceDescriptor

class CythonScope(ModuleScope):
    is_cython_builtin = 1

    def __init__(self):
        ModuleScope.__init__(self, u'cython', None, None)
        self.pxd_file_loaded = True
        self.populate_cython_scope()

    def lookup_type(self, name):
        # This function should go away when types are all first-level objects.
        type = parse_basic_type(name)
        if type:
            return type

    def find_module(self, module_name, pos):
        error("cython.%s is not available" % module_name, pos)

    def find_submodule(self, module_name):
        entry = self.entries.get(module_name, None)
        if entry and entry.as_module:
            return entry.as_module
        else:
            # TODO: fix find_submodule control flow so that we're not
            # expected to create a submodule here (to protect CythonScope's
            # possible immutability). Hack ourselves out of the situation
            # for now.
            raise error((StringSourceDescriptor(u"cython", u""), 0, 0),
                  "cython.%s is not available" % module_name)

    def lookup_qualified_name(self, qname):
        # ExprNode.as_cython_attribute generates qnames and we untangle it here...
        name_path = qname.split(u'.')
        scope = self
        while len(name_path) > 1:
            scope = scope.lookup_here(name_path[0]).as_module
            del name_path[0]
            if scope is None:
                return None
        else:
            return scope.lookup_here(name_path[0])

    def populate_cython_scope(self):
        # These are used to optimize isinstance in FinalOptimizePhase
        type_object = self.declare_typedef(
            'PyTypeObject',
            base_type = c_void_type,
            pos = None,
            cname = 'PyTypeObject')
        type_object.is_void = True
        type_object_type = type_object.type

        self.declare_cfunction(
            'PyObject_TypeCheck',
            CFuncType(c_bint_type, [CFuncTypeArg("o", py_object_type, None),
                                    CFuncTypeArg("t", c_ptr_type(type_object_type), None)]),
            pos = None,
            defining = 1,
            cname = 'PyObject_TypeCheck')

#        self.test_cythonscope()

    def test_cythonscope(self):
        # A special function just to make it easy to test the scope and
        # utility code functionality in isolation. It is available to
        # "end-users" but nobody will know it is there anyway...
        cython_testscope_utility_code.declare_in_scope(self)
        cython_test_extclass_utility_code.declare_in_scope(self)

        #
        # The view sub-scope
        #
        self.viewscope = viewscope = ModuleScope(u'cython.view', self, None)
        self.declare_module('view', viewscope, None)
        viewscope.is_cython_builtin = True
        viewscope.pxd_file_loaded = True

        cythonview_testscope_utility_code.declare_in_scope(viewscope)

        for x in ('strided', 'contig', 'follow', 'direct', 'ptr', 'full'):
            entry = viewscope.declare_var(x, py_object_type, None,
                                          cname='__pyx_viewaxis_%s' % x,
                                          is_cdef=True)
            entry.utility_code_definition = view_utility_code

def create_cython_scope(context, create_testscope):
    # One could in fact probably make it a singleton,
    # but not sure yet whether any code mutates it (which would kill reusing
    # it across different contexts)
    scope = CythonScope()

    if create_testscope:
        scope.test_cythonscope()

    return scope


cython_testscope_utility_code = CythonUtilityCode(u"""
@cname('__pyx_testscope')
cdef object _testscope(int value):
    return "hello from cython scope, value=%d" % value
""")

undecorated_methods_protos = UtilityCode(proto=u"""
    /* These methods are undecorated and have therefore no prototype */
    static PyObject *__pyx_TestClass_cdef_method(
            struct __pyx_TestClass *self, int value);
    static PyObject *__pyx_TestClass_cpdef_method(
            struct __pyx_TestClass *self, int value, int skip_dispatch);
    static PyObject *__pyx_TestClass_def_method(
            PyObject *self, PyObject *value);
""")

test_cython_utility_dep = CythonUtilityCode(u"""
@cname('__pyx_test_dep')
cdef test_dep(obj):
    print 'test_dep', obj
""")

cython_test_extclass_utility_code = CythonUtilityCode(
        name="TestClassUtilityCode",
        prefix="__pyx_prefix_TestClass_",
        requires=[undecorated_methods_protos, test_cython_utility_dep],
        impl=u"""
cdef extern from *:
    cdef object __pyx_test_dep(object)

@cname('__pyx_TestClass')
cdef class TestClass(object):
    cdef public int value

    def __init__(self, int value):
        self.value = value

    def __str__(self):
        return 'TestClass(%d)' % self.value

    cdef cdef_method(self, int value):
        print 'Hello from cdef_method', value

    cpdef cpdef_method(self, int value):
        print 'Hello from cpdef_method', value

    def def_method(self, int value):
        print 'Hello from def_method', value

    @cname('cdef_cname')
    cdef cdef_cname_method(self, int value):
        print "Hello from cdef_cname_method", value

    @cname('cpdef_cname')
    cpdef cpdef_cname_method(self, int value):
        print "Hello from cpdef_cname_method", value

    @cname('def_cname')
    def def_cname_method(self, int value):
        print "Hello from def_cname_method", value

@cname('__pyx_test_call_other_cy_util')
cdef test_call(obj):
    print 'test_call'
    __pyx_test_dep(obj)

@cname('__pyx_TestClass_New')
cdef _testclass_new(int value):
    return TestClass(value)
""")


cythonview_testscope_utility_code = CythonUtilityCode(u"""
@cname('__pyx_view_testscope')
cdef object _testscope(int value):
    return "hello from cython.view scope, value=%d" % value
""")

view_utility_code = CythonUtilityCode(u"""
cdef class Enum:
    cdef object name
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

cdef strided = Enum("<strided axis packing mode>")
cdef contig = Enum("<contig axis packing mode>")
cdef follow = Enum("<follow axis packing mode>")
cdef direct = Enum("<direct axis access mode>")
cdef ptr = Enum("<ptr axis access mode>")
cdef full = Enum("<full axis access mode>")
""", prefix="__pyx_viewaxis_")