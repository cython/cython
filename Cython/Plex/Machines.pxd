cimport cython

from .Actions cimport Action
from .Transitions cimport TransitionMap

cdef i32 maxint

@cython.final
cdef class Machine:
    cdef readonly list states
    cdef readonly dict initial_states
    cdef readonly isize next_state_number

    cpdef new_state(self)
    cpdef new_initial_state(self, name)

@cython.final
cdef class Node:
    cdef readonly TransitionMap transitions
    cdef readonly Action action
    pub dict epsilon_closure
    cdef readonly isize number
    cdef readonly i32 action_priority

@cython.final
cdef class FastMachine:
    cdef readonly dict initial_states
    cdef readonly dict new_state_template
    cdef readonly list states
    cdef readonly isize next_number
