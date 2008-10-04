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
                                                  
    def lookup_type(self, name):
        # This function should go away when types are all first-level objects. 
        type = parse_basic_type(name)
        if type:
            return type

def create_cython_scope(context):
    return CythonScope(context)
