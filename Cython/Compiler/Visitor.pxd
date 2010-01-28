cimport cython

cdef class BasicVisitor:
    cdef dict dispatch_table
    cpdef visit(self, obj)
    cpdef find_handler(self, obj)

cdef class TreeVisitor(BasicVisitor):
    cdef public list access_path
    cpdef visitchild(self, child, parent, attrname, idx)
    @cython.locals(idx=int)
    cpdef dict _visitchildren(self, parent, attrs)
#    cpdef visitchildren(self, parent, attrs=*)

cdef class VisitorTransform(TreeVisitor):
    cpdef visitchildren(self, parent, attrs=*)
    cpdef recurse_to_children(self, node)

cdef class CythonTransform(VisitorTransform):
    cdef public context
    cdef public current_directives
