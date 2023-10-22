# cython: language_level=3

import cython

from ..Plex.Scanners cimport Scanner

cdef unicode any_string_prefix, IDENT

cdef get_lexicon()
cdef initial_compile_time_env()

## methods commented with '##' out are used by Parsing.py when compiled.

@cython.final
cdef class CompileTimeScope:
    cdef pub dict entries
    cdef pub CompileTimeScope outer
    ##cdef declare(self, name, value)
    ##cdef lookup_here(self, name)
    ##cpdef lookup(self, name)

@cython.final
cdef class PyrexScanner(Scanner):
    cdef pub context
    cdef pub list included_files
    cdef pub CompileTimeScope compile_time_env
    cdef pub bint compile_time_eval
    cdef pub bint compile_time_expr
    cdef pub bint parse_comments
    cdef pub bint in_python_file
    cdef pub source_encoding
    cdef dict keywords
    cdef pub list indentation_stack
    cdef pub indentation_char
    cdef pub int bracket_nesting_level
    cdef readonly bint async_enabled
    cdef pub unicode sy
    cdef pub systring  # EncodedString
    cdef pub list put_back_on_failure

    cdef isize current_level(self)
    #cpdef commentline(self, text)
    #cpdef open_bracket_action(self, text)
    #cpdef close_bracket_action(self, text)
    #cpdef newline_action(self, text)
    #cpdef begin_string_action(self, text)
    #cpdef end_string_action(self, text)
    #cpdef unclosed_string_action(self, text)
    @cython.locals(current_level=isize, new_level=isize)
    cpdef indentation_action(self, text)
    #cpdef eof_action(self, text)
    ##cdef next(self)
    ##cdef peek(self)
    #cpdef put_back(self, sy, systring)
    ##cdef bint expect(self, what, message = *) except -2
    ##cdef expect_keyword(self, what, message = *)
    ##cdef expected(self, what, message = *)
    ##cdef expect_indent(self)
    ##cdef expect_dedent(self)
    ##cdef expect_newline(self, message=*, bint ignore_semicolon=*)
    ##cdef int enter_async(self) except -1
    ##cdef int exit_async(self) except -1
    cdef void error_at_scanpos(self, str message) except *
