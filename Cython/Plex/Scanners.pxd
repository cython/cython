from __future__ import absolute_import

import cython

from Cython.Plex.Actions cimport Action

cdef class Scanner:
    pub lexicon
    pub stream
    pub name
    pub unicode buffer
    pub isize buf_start_pos
    pub isize next_pos
    pub isize cur_pos
    pub isize cur_line
    pub isize cur_line_start
    pub isize start_pos
    cdef tuple current_scanner_position_tuple
    pub tuple last_token_position_tuple
    pub text
    pub initial_state # int?
    pub state_name
    pub list queue
    pub bint trace
    pub cur_char
    pub i64 input_state

    pub level

    @cython.locals(input_state=i64)
    fn inline next_char(self)

    @cython.locals(action=Action)
    cpdef tuple read(self)

    fn inline unread(self, token, value, position)

    fn inline get_current_scan_pos(self)

    fn inline tuple scan_a_token(self)

    ##cdef tuple position(self)  # used frequently by Parsing.py

    @cython.final
    @cython.locals(cur_pos=isize, cur_line=isize, cur_line_start=isize,
                   input_state=i64, next_pos=isize, state=dict,
                   buf_start_pos=isize, buf_len=isize, buf_index=isize,
                   trace=bint, discard=isize, data=unicode, buffer=unicode)
    fn run_machine_inlined(self)

    fn inline begin(self, state)
    
    fn inline produce(self, value, text = *)
