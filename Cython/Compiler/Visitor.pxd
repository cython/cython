cdef class BasicVisitor:
    cdef dict dispatch_table
    cpdef visit(self, obj)

cdef class TreeVisitor(BasicVisitor):
    cdef public list access_path
    cpdef visitchild(self, child, parent, attrname, idx)

cdef class VisitorTransform(TreeVisitor):
    cdef object _super_visitchildren
    cpdef visitchildren(self, parent, attrs=*)
    cpdef recurse_to_children(self, node)

cdef class CythonTransform(VisitorTransform):
    cdef public context
    cdef public current_directives
