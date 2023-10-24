# cython: language_level=3str

cimport cython

from .Visitor cimport (
    CythonTransform, VisitorTransform, TreeVisitor,
    ScopeTrackingTransform, EnvTransform)

# Don't include mixins, only the main classes.
#cdef class SkipDeclarations:

cdef class NormalizeTree(CythonTransform):
    cdef bint is_in_statlist
    cdef bint is_in_expr
    cpdef visit_StatNode(self, node, is_listcontainer=*)

cdef class PostParse(ScopeTrackingTransform):
    cdef dict specialattribute_handlers
    cdef usize lambda_counter
    cdef usize genexpr_counter
    fn _visit_assignment_node(self, node, list expr_list)

# def eliminate_rhs_duplicates(list expr_list_list, list ref_node_sequence)
# def sort_common_subsequences(list items)
#[cython.locals(starred_targets=isize, lhs_size=isize, rhs_size=isize)]
fn flatten_parallel_assignments(list input, list output)
fn map_starred_assignment(list lhs_targets, list starred_assignments, list lhs_args, list rhs_args)

# class PxdPostParse(CythonTransform, SkipDeclarations):
# class InterpretCompilerDirectives(CythonTransform, SkipDeclarations):
# class WithTransform(VisitorTransform, SkipDeclarations):
# class DecoratorTransform(CythonTransform, SkipDeclarations):

# class AnalyseDeclarationsTransform(EnvTransform):

cdef class AnalyseExpressionsTransform(CythonTransform):
    pass

cdef class ExpandInplaceOperators(EnvTransform):
    pass

cdef class AlignFunctionDefinitions(CythonTransform):
    cdef dict directives
    cdef set imported_names
    cdef object scope

#[cython.final]
cdef class YieldNodeCollector(TreeVisitor):
    pub list yields
    pub list returns
    pub list finallys
    pub list excepts
    pub bint has_return_value
    pub bint has_yield
    pub bint has_await

#[cython.final]
cdef class MarkClosureVisitor(CythonTransform):
    cdef bint needs_closure

#[cython.final]
cdef class CreateClosureClasses(CythonTransform):
    cdef list path
    cdef bint in_lambda
    cdef module_scope
    cdef generator_class

    fn create_class_from_scope(self, node, target_module_scope, inner_node=*)
    fn find_entries_used_in_closures(self, node)

#cdef class InjectGilHandling(VisitorTransform, SkipDeclarations):
#    cdef bint nogil

cdef class GilCheck(VisitorTransform):
    cdef list env_stack
    cdef bint nogil
    cdef bint nogil_declarator_only
    cdef bint current_gilstat_node_knows_gil_state

cdef class TransformBuiltinMethods(EnvTransform):
    fn visit_cython_attribute(self, node)
