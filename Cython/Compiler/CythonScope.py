from Symtab import ModuleScope
from PyrexTypes import *
from UtilityCode import CythonUtilityCode

class CythonScope(ModuleScope):
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
        error("cython.%s is not available" % module_name)

    def populate_cython_scope(self):
        # These are used to optimize isinstance in FinalOptimizePhase
        type_object = self.declare_typedef(
            'PyTypeObject', 
            base_type = c_void_type, 
            pos = None,
            cname = 'PyTypeObject')
        type_object.is_void = True
        
        self.declare_cfunction(
            'PyObject_TypeCheck',
            CFuncType(c_bint_type, [CFuncTypeArg("o", py_object_type, None),
                                    CFuncTypeArg("t", c_ptr_type(type_object), None)]),
            pos = None,
            defining = 1,
            cname = 'PyObject_TypeCheck')

        #
        # A special function just to make it easy to test the scope and
        # utility code functionality in isolation. It is available to
        # "end-users" but nobody will know it is there anyway...
        #
        testcythonscope = self.declare_cfunction(
            '_testcythonscope',
            CFuncType(py_object_type, [CFuncTypeArg("value", c_int_type, None)]),
            pos=None,
            defining=1,
            cname='__pyx_cython__testcythonscope'
        )
        testcythonscope.utility_code_definition = cython_testscope_utility_code

def create_cython_scope(context):
    # One could in fact probably make it a singleton,
    # but not sure yet whether any code mutates it (which would kill reusing
    # it across different contexts)
    return CythonScope()

cython_testscope_utility_code = CythonUtilityCode(u"""
cdef object _testcythonscope(int value):
    return "hello value=%d" % value
""", name="cython utility code", prefix="__pyx_cython_")
