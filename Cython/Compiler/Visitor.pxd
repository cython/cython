cimport cython

cdef class BasicVisitor:
    cdef dict dispatch_table
    cpdef visit(self, obj)
    cdef _visit(self, obj)
    cdef find_handler(self, obj)

cdef class TreeVisitor(BasicVisitor):
    cdef public list access_path
    cdef _visitchild(self, child, parent, attrname, idx)
    @cython.locals(idx=int)
    cdef dict _visitchildren(self, parent, attrs)
    cpdef visitchildren(self, parent, attrs=*)

cdef class VisitorTransform(TreeVisitor):
    cpdef visitchildren(self, parent, attrs=*)
    cpdef recurse_to_children(self, node)

cdef class CythonTransform(VisitorTransform):
    cdef public context
    cdef public current_directives

cdef class EnvTransform(CythonTransform):
    cdef public list env_stack
