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

        # A special function just to make it easy to test the scope and
        # utility code functionality in isolation. It is available to
        # "end-users" but nobody will know it is there anyway...
        entry = self.declare_cfunction(
            '_testscope',
            CFuncType(py_object_type, [CFuncTypeArg("value", c_int_type, None)]),
            pos=None,
            defining=1,
            cname='__pyx_cython__testscope'
        )
        entry.utility_code_definition = cython_testscope_utility_code

        #
        # The view sub-scope
        #
        self.viewscope = viewscope = ModuleScope(u'cython.view', self, None)
        self.declare_module('view', viewscope, None)
        viewscope.is_cython_builtin = True
        viewscope.pxd_file_loaded = True
        entry = viewscope.declare_cfunction(
            '_testscope',
            CFuncType(py_object_type, [CFuncTypeArg("value", c_int_type, None)]),
            pos=None,
            defining=1,
            cname='__pyx_cython_view__testscope'
        )
        entry.utility_code_definition = cythonview_testscope_utility_code

def create_cython_scope(context):
    # One could in fact probably make it a singleton,
    # but not sure yet whether any code mutates it (which would kill reusing
    # it across different contexts)
    return CythonScope()

cython_testscope_utility_code = CythonUtilityCode(u"""
cdef object _testscope(int value):
    return "hello from cython scope, value=%d" % value
""", name="cython utility code", prefix="__pyx_cython_")

cythonview_testscope_utility_code = CythonUtilityCode(u"""
cdef object _testscope(int value):
    return "hello from cython.view scope, value=%d" % value
""", name="cython utility code", prefix="__pyx_cython_view_")
