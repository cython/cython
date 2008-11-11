cdef class Scanner:
    cdef public lexicon
    cdef public stream
    cdef public name
    cdef public buffer
    cdef public long buf_start_pos
    cdef public long next_pos
    cdef public long cur_pos
    cdef public long cur_line
    cdef public long cur_line_start
    cdef public long start_pos
    cdef public long start_line
    cdef public long start_col
    cdef public text
    cdef public initial_state
    cdef public state_name
    cdef public list queue
    cdef public bint trace
    cdef public cur_char
    cdef public input_state
    
    cdef public level
    