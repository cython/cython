# cython: language_level=3

cimport cython

from .Visitor cimport CythonTransform, TreeVisitor

cdef class ControlBlock:
    cdef pub set children
    cdef pub set parents
    cdef pub set positions
    cdef pub list stats
    cdef pub dict gen
    cdef pub set bounded

    # Big integer bitsets
    cdef pub object i_input
    cdef pub object i_output
    cdef pub object i_gen
    cdef pub object i_kill
    cdef pub object i_state

    cpdef bint empty(self)
    cpdef detach(self)
    cpdef add_child(self, block)

cdef class ExitBlock(ControlBlock):
    cpdef bint empty(self)

cdef class NameAssignment:
    cdef pub bint is_arg
    cdef pub bint is_deletion
    cdef pub object lhs
    cdef pub object rhs
    cdef pub object entry
    cdef pub object pos
    cdef pub set refs
    cdef pub object bit
    cdef pub object inferred_type
    cdef pub object rhs_scope

cdef class AssignmentList:
    cdef pub object bit
    cdef pub object mask
    cdef pub list stats

cdef class AssignmentCollector(TreeVisitor):
    cdef list assignments

@cython.final
cdef class ControlFlow:
    cdef pub set blocks
    cdef pub set entries
    cdef pub list loops
    cdef pub list exceptions

    cdef pub ControlBlock entry_point
    cdef pub ExitBlock exit_point
    cdef pub ControlBlock block

    cdef pub dict assmts

    cdef pub Py_ssize_t in_try_block

    cpdef newblock(self, ControlBlock parent=*)
    cpdef nextblock(self, ControlBlock parent=*)
    cpdef bint is_tracked(self, entry)
    cpdef bint is_statically_assigned(self, entry)
    cpdef mark_position(self, node)
    cpdef mark_assignment(self, lhs, rhs, entry, rhs_scope=*)
    cpdef mark_argument(self, lhs, rhs, entry)
    cpdef mark_deletion(self, node, entry)
    cpdef mark_reference(self, node, entry)

    @cython.locals(block=ControlBlock, parent=ControlBlock, unreachable=set)
    cpdef normalize(self)

    @cython.locals(bit=object, assmts=AssignmentList, block=ControlBlock)
    cpdef initialize(self)

    @cython.locals(assmts=AssignmentList, assmt=NameAssignment)
    cpdef set map_one(self, istate, entry)

    @cython.locals(block=ControlBlock, parent=ControlBlock)
    cdef reaching_definitions(self)

cdef class Uninitialized:
    pass

cdef class Unknown:
    pass

cdef class MessageCollection:
    cdef set messages

@cython.locals(dirty=bint, block=ControlBlock, parent=ControlBlock,
               assmt=NameAssignment)
cdef check_definitions(ControlFlow flow, dict compiler_directives)

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

    cpdef mark_assignment(self, lhs, rhs=*, rhs_scope=*)
    cpdef mark_position(self, node)
