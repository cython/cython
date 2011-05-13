from Symtab import ModuleScope
from PyrexTypes import *

shape_func_type = CFuncType(
    c_ptr_type(c_py_ssize_t_type),
    [CFuncTypeArg("buffer", py_object_type, None)])

class CythonScope(ModuleScope):
    def __init__(self, context):
        ModuleScope.__init__(self, u'cython', None, context)
        self.pxd_file_loaded = True

        self.shape_entry = self.declare_cfunction('shape',
                                                  shape_func_type,
                                                  pos=None,
                                                  defining = 1,
                                                  cname='<error>')

        for fused_type in (cy_integral_type, cy_floating_type, cy_numeric_type):
            entry = self.declare_typedef(fused_type.name,
                                         fused_type,
                                         None,
                                         cname='<error>')
            entry.in_cinclude = True

    def lookup_type(self, name):
        # This function should go away when types are all first-level objects.
        type = parse_basic_type(name)
        if type:
            return type

        return super(CythonScope, self).lookup_type(name)

def create_cython_scope(context):
    create_utility_scope(context)
    return CythonScope(context)


def create_utility_scope(context):
    global utility_scope
    utility_scope = ModuleScope(u'utility', None, context)

    # These are used to optimize isinstance in FinalOptimizePhase
    type_object = utility_scope.declare_typedef('PyTypeObject',
                                                base_type = c_void_type,
                                                pos = None,
                                                cname = 'PyTypeObject')
    type_object.is_void = True

    utility_scope.declare_cfunction(
                'PyObject_TypeCheck',
                CFuncType(c_bint_type, [CFuncTypeArg("o", py_object_type, None),
                                        CFuncTypeArg("t", c_ptr_type(type_object), None)]),
                pos = None,
                defining = 1,
                cname = 'PyObject_TypeCheck')

    return utility_scope
