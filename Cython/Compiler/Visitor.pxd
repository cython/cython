cimport cython

cdef class TreeVisitor:
    cdef public list access_path
    cdef dict dispatch_table

    cpdef visit(self, obj)
    cdef _visit(self, obj)
    cdef find_handler(self, obj)
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

cdef class ScopeTrackingTransform(CythonTransform):
    cdef public scope_type
    cdef public scope_node
    cdef visit_scope(self, node, scope_type)

cdef class EnvTransform(CythonTransform):
    cdef public list env_stack

cdef class MethodDispatcherTransform(EnvTransform):
    cdef _find_handler(self, match_name, bint has_kwargs)
    cdef _dispatch_to_handler(self, node, function, arg_list, kwargs=*)

cdef class RecursiveNodeReplacer(VisitorTransform):
     cdef public orig_node
     cdef public new_node
