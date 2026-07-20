cimport cython

from .Visitor cimport CythonTransform, TreeVisitor

cdef class ControlBlock:
    cdef readonly set[ControlBlock] children
    cdef readonly set[ControlBlock] parents
    cdef readonly set positions
    cdef readonly list stats
    cdef readonly dict gen
    cdef readonly set bounded

    # Big integer bitsets
    cdef object i_input
    cdef object i_output
    cdef object i_gen
    cdef object i_kill
    cdef object i_state

    cpdef bint empty(self)
    cpdef detach(self)
    cpdef add_child(self, block)

cdef class ExitBlock(ControlBlock):
    cpdef bint empty(self)

cdef class NameAssignment:
    cdef public bint is_arg
    cdef public bint is_deletion
    cdef public object bit
    cdef public object inferred_type
    cdef readonly object lhs
    cdef readonly object rhs
    cdef readonly object entry
    cdef readonly object pos
    cdef readonly set refs
    cdef readonly object rhs_scope
    cdef readonly object assignment_type

@cython.final
cdef class AssignmentList:
    cdef object bit
    cdef object mask
    cdef list[NameAssignment] stats

cdef class AssignmentCollector(TreeVisitor):
    cdef list[tuple] assignments

@cython.final
cdef class LoopDescr:
    cdef ControlBlock next_block
    cdef ControlBlock loop_block
    cdef list[ExceptionDescr] exceptions

@cython.final
cdef class ExceptionDescr:
    cdef ControlBlock entry_point
    cdef ControlBlock finally_enter
    cdef ControlBlock finally_exit

@cython.final
cdef class ControlFlow:
    cdef set[ControlBlock] blocks
    cdef set entries
    cdef list[LoopDescr] loops
    cdef list[ExceptionDescr] exceptions

    cdef ControlBlock entry_point
    cdef ExitBlock exit_point
    cdef ControlBlock block

    cdef dict[object, AssignmentList] assmts

    cdef Py_ssize_t in_try_block

    cpdef ControlBlock newblock(self, ControlBlock parent=*)
    cpdef ControlBlock nextblock(self, ControlBlock parent=*)
    cpdef bint is_tracked(self, entry)
    cpdef bint is_statically_assigned(self, entry)
    cpdef mark_position(self, node)
    cpdef mark_assignment(self, lhs, rhs, entry, rhs_scope=*, assignment_type=*)
    cpdef mark_argument(self, lhs, rhs, entry)
    cpdef mark_deletion(self, node, entry)
    cpdef mark_reference(self, node, entry)
    cpdef normalize(self)
    cpdef initialize(self)
    cpdef set map_one(self, istate, entry)
    cdef reaching_definitions(self)

cdef class Uninitialized:
    pass

cdef class Unknown:
    pass

cdef class MessageCollection:
    cdef set messages

@cython.final
cdef class ControlFlowAnalysis(CythonTransform):
    cdef object gv_ctx
    cdef object constant_folder
    cdef set reductions
    cdef list stack  # a stack of (env, flow) tuples
    cdef object env
    cdef ControlFlow flow
    cdef object object_expr
    cdef bint in_inplace_assignment
    cdef bint in_assignment_expression

    cpdef mark_assignment(self, lhs, rhs=*, rhs_scope=*, assignment_type=*)
    cpdef mark_position(self, node)
