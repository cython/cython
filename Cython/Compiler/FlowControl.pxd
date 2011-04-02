cimport cython

cdef class ControlBlock:
     cdef public set children
     cdef public set parents
     cdef public set positions
     cdef public list stats
     cdef public dict gen
     cdef public set bounded
     cdef public dict input
     cdef public dict output

     cpdef bint empty(self)
     cpdef detach(self)
     cpdef add_child(self, block)

cdef class ExitBlock(ControlBlock):
     cpdef bint empty(self)

cdef class ControlFlow:
     cdef public set blocks
     cdef public set entries
     cdef public list loops
     cdef public list exceptions

     cdef public ControlBlock entry_point
     cdef public ExitBlock exit_point
     cdef public ControlBlock block

     cpdef newblock(self, parent=*)
     cpdef nextblock(self, parent=*)
     cpdef bint is_tracked(self, entry)
     cpdef mark_position(self, node)
     cpdef mark_assignment(self, lhs, rhs, entry=*)
     cpdef mark_argument(self, lhs, rhs, entry)
     cpdef mark_deletion(self, node, entry)
     cpdef mark_reference(self, node, entry)
     cpdef normalize(self)

cdef class Uninitialized:
     pass

@cython.locals(dirty=bint, block=ControlBlock, parent=ControlBlock)
cdef check_definitions(ControlFlow flow, dict compiler_directives)
