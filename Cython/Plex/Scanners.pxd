from __future__ import absolute_import

import cython

from Cython.Plex.Actions cimport Action

cdef class Scanner:

    cdef pub lexicon
    cdef pub stream
    cdef pub name
    cdef pub unicode buffer
    cdef pub Py_ssize_t buf_start_pos
    cdef pub Py_ssize_t next_pos
    cdef pub Py_ssize_t cur_pos
    cdef pub Py_ssize_t cur_line
    cdef pub Py_ssize_t cur_line_start
    cdef pub Py_ssize_t start_pos
    cdef tuple current_scanner_position_tuple
    cdef pub tuple last_token_position_tuple
    cdef pub text
    cdef pub initial_state # int?
    cdef pub state_name
    cdef pub list queue
    cdef pub bint trace
    cdef pub cur_char
    cdef pub long input_state

    cdef pub level

    @cython.locals(input_state=long)
    cdef inline next_char(self)
    @cython.locals(action=Action)
    cpdef tuple read(self)
    cdef inline unread(self, token, value, position)
    cdef inline get_current_scan_pos(self)
    cdef inline tuple scan_a_token(self)
    ##cdef tuple position(self)  # used frequently by Parsing.py

    @cython.final
    @cython.locals(cur_pos=Py_ssize_t, cur_line=Py_ssize_t, cur_line_start=Py_ssize_t,
                   input_state=long, next_pos=Py_ssize_t, state=dict,
                   buf_start_pos=Py_ssize_t, buf_len=Py_ssize_t, buf_index=Py_ssize_t,
                   trace=bint, discard=Py_ssize_t, data=unicode, buffer=unicode)
    cdef run_machine_inlined(self)

    cdef inline begin(self, state)
    cdef inline produce(self, value, text = *)
