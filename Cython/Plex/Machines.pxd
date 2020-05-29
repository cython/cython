cimport cython

@cython.final
cdef class Node:
    cdef readonly object transitions  # TransitionMap
    cdef readonly object action  # Action
    cdef public object epsilon_closure  # dict
    cdef readonly Py_ssize_t number
    cdef readonly long action_priority


@cython.final
cdef class FastMachine:
    cdef readonly dict initial_states
    cdef readonly dict new_state_template
    cdef readonly list states
    cdef readonly Py_ssize_t next_number
