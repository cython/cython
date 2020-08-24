
cdef extern from "<execution>" namespace "std::execution" nogil:
    cdef cppclass sequenced_policy:
        pass
    cdef cppclass parallel_policy:
        parallel_policy()
    cdef cppclass parallel_unsequenced_policy:
        pass
    cdef cppclass unsequenced_policy:
        pass
    
    sequenced_policy seq "std::execution::seq"
    parallel_policy par "std::execution::par"
    parallel_unsequenced_policy par_unseq "std::execution::par_unseq"
    unsequenced_policy unseq "std::execution::unseq"
