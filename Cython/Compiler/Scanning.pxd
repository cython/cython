import cython

from ..Plex.Scanners cimport Scanner

cdef unicode any_string_prefix, IDENT

cdef get_lexicon()
cdef initial_compile_time_env()

## methods commented with '##' out are used by Parsing.py when compiled.

@cython.final
cdef class CompileTimeScope:
    cdef public dict entries
    cdef public CompileTimeScope outer
    ##cdef declare(self, name, value)
    ##cdef lookup_here(self, name)
    ##cpdef lookup(self, name)

@cython.final
cdef class PyrexScanner(Scanner):
    cdef public context
    cdef public list included_files
    cdef public CompileTimeScope compile_time_env
    cdef public bint compile_time_eval
    cdef public bint compile_time_expr
    cdef public bint parse_comments
    cdef public bint in_python_file
    cdef public source_encoding
    cdef dict keywords
    cdef public list[Py_ssize_t] indentation_stack
    cdef public Py_UCS4 indentation_char
    cdef public Py_ssize_t bracket_nesting_level
    cdef readonly bint async_enabled
    cdef public unicode sy
    cdef public systring  # EncodedString
    cdef public list put_back_on_failure
    # fstrings/tstrings
    cdef list[FTStringState] ft_string_state_stack
    cdef int in_ft_string_expr_prescan

    cdef Py_ssize_t current_level(self)

    cpdef int next(self) except -1
    cpdef tuple[unicode, object] peek(self)
    cpdef int error_at_scanpos(self, message) except -1
    cpdef int expect(self, what: str, message=*) except -1
    cpdef int expect_keyword(self, what: str, message=*) except -1
    cpdef int expected(self, what: str, message=*)  except -1
    cpdef int expect_indent(self) except -1
    cpdef int expect_dedent(self) except -1
    cpdef int expect_newline(self, message=*, ignore_semicolon: bint=*) except -1
    cpdef int enter_async(self) except -1
    cpdef int exit_async(self) except -1


cdef class FTStringState:
    cdef list[FTStringBracketState] bracket_states
    cdef readonly str scanner_state

    cdef bracket_nesting_level(self)
    cdef bint in_format_specifier(self)
    cdef set_in_format_specifier(self)
    cdef push_bracket_state(self, Py_ssize_t bracket_nesting_level)
    cdef pop_bracket_state(self)

@cython.final
cdef class FTStringBracketState:
    cdef Py_ssize_t bracket_nesting_level
    cdef bint in_format_specifier
