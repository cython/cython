# cython: language_level=3str

cimport cython

cdef class TreeVisitor:
    pub list access_path
    cdef dict dispatch_table

    cpdef visit(self, obj)

    fn _visit(self, obj)

    fn find_handler(self, obj)

    fn _visitchild(self, child, parent, attrname, idx)

    fn dict _visitchildren(self, parent, attrs, exclude)

    cpdef visitchildren(self, parent, attrs=*, exclude=*)

    fn _raise_compiler_error(self, child, e)

cdef class VisitorTransform(TreeVisitor):
    fn dict _process_children(self, parent, attrs=*, exclude=*)

    cpdef visitchildren(self, parent, attrs=*, exclude=*)

    fn list _flatten_list(self, list orig_list)

    cpdef visitchild(self, parent, str attr, idx=*)

cdef class CythonTransform(VisitorTransform):
    pub context
    pub current_directives

cdef class ScopeTrackingTransform(CythonTransform):
    pub scope_type
    pub scope_node

    fn visit_scope(self, node, scope_type)

cdef class EnvTransform(CythonTransform):
    pub list env_stack

cdef class MethodDispatcherTransform(EnvTransform):
    #[cython.final]
    fn _visit_binop_node(self, node)

    #[cython.final]
    fn _find_handler(self, match_name, bint has_kwargs)

    #[cython.final]
    fn _delegate_to_assigned_value(self, node, function, arg_list, kwargs)

    #[cython.final]
    fn _dispatch_to_handler(self, node, function, arg_list, kwargs)

    #[cython.final]
    fn _dispatch_to_method_handler(self, attr_name, self_arg,
                                   is_unbound_method, type_name,
                                   node, function, arg_list, kwargs)

cdef class RecursiveNodeReplacer(VisitorTransform):
    pub orig_node
    pub new_node

cdef class NodeFinder(TreeVisitor):
    cdef node
    pub bint found
