import cython

from Cython.Plex.Scanners cimport Scanner

cdef class CompileTimeScope:
    cdef public entries
    cdef public outer

cdef class PyrexScanner(Scanner):
    cdef public context
    cdef public list included_files
    cdef public compile_time_env
    cdef public bint compile_time_eval
    cdef public bint compile_time_expr
    cdef public bint parse_comments
    cdef public source_encoding
    cdef public list indentation_stack
    cdef public indentation_char
    cdef public int bracket_nesting_level
    cdef public sy
    cdef public systring

    cdef long current_level(self)
    cpdef begin(self, state)
    cpdef next(self)
    cpdef bint expect(self, what, message = *) except -2
    
    @cython.locals(current_level=cython.long, new_level=cython.long)
    cpdef indentation_action(self, text)
