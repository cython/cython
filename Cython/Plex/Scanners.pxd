import cython

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
    cdef public initial_state # int?
    cdef public state_name
    cdef public list queue
    cdef public bint trace
    cdef public cur_char
    cdef public input_state

    cdef public level

    @cython.locals(input_state=long)
    cpdef next_char(self)
    cpdef read(self)
    cpdef position(self)

    @cython.locals(cur_pos=cython.long, cur_line=cython.long,
                 cur_line_start=cython.long, input_state=cython.long,
                 next_pos=cython.long, buf_start_pos=cython.long,
                 buf_len=cython.long, buf_index=cython.long,
                 trace=cython.bint, discard=cython.long)
    cpdef run_machine_inlined(self)
    
    cpdef begin(self, state)
    cpdef produce(self, value, text = *)
