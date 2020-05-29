cdef class FastMachine:
    cdef readonly dict initial_states
    cdef readonly dict new_state_template
    cdef readonly list states
    cdef readonly Py_ssize_t next_number
