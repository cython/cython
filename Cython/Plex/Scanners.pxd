from __future__ import absolute_import

import cython

from Cython.Plex.Actions cimport Action

cdef class Scanner:
    cdef pub lexicon
    cdef pub stream
    cdef pub name
    cdef pub unicode buffer
    cdef pub isize buf_start_pos
    cdef pub isize next_pos
    cdef pub isize cur_pos
    cdef pub isize cur_line
    cdef pub isize cur_line_start
    cdef pub isize start_pos
    cdef tuple current_scanner_position_tuple
    cdef pub tuple last_token_position_tuple
    cdef pub text
    cdef pub initial_state # int?
    cdef pub state_name
    cdef pub list queue
    cdef pub bint trace
    cdef pub cur_char
    cdef pub i64 input_state

    cdef pub level

    @cython.locals(input_state=i64)
    cdef inline next_char(self)
    @cython.locals(action=Action)
    cpdef tuple read(self)
    cdef inline unread(self, token, value, position)
    cdef inline get_current_scan_pos(self)
    cdef inline tuple scan_a_token(self)
    ##cdef tuple position(self)  # used frequently by Parsing.py

    @cython.final
    @cython.locals(cur_pos=isize, cur_line=isize, cur_line_start=isize,
                   input_state=i64, next_pos=isize, state=dict,
                   buf_start_pos=isize, buf_len=isize, buf_index=isize,
                   trace=bint, discard=isize, data=unicode, buffer=unicode)
    cdef run_machine_inlined(self)

    cdef inline begin(self, state)
    cdef inline produce(self, value, text = *)
