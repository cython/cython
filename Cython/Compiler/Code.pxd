# cython: language_level=3

cimport cython
from ..StringIOTree cimport StringIOTree

cdef class UtilityCodeBase(object):
    cpdef format_code(self, code_string, replace_empty_lines=*)

cdef class UtilityCode(UtilityCodeBase):
    cdef pub object name
    cdef pub object proto
    cdef pub object impl
    cdef pub object init
    cdef pub object cleanup
    cdef pub object proto_block
    cdef pub object requires
    cdef pub dict _cache
    cdef pub list specialize_list
    cdef pub object file

    cpdef none_or_sub(self, s, context)

cdef class FunctionState:
    cdef pub set names_taken
    cdef pub object owner
    cdef pub object scope

    cdef pub object error_label
    cdef pub size_t label_counter
    cdef pub set labels_used
    cdef pub object return_label
    cdef pub object continue_label
    cdef pub object break_label
    cdef pub list yield_labels

    cdef pub object return_from_error_cleanup_label # not used in __init__ ?

    cdef pub object exc_vars
    cdef pub object current_except
    cdef pub bint in_try_finally
    cdef pub bint can_trace
    cdef pub bint gil_owned

    cdef pub list temps_allocated
    cdef pub dict temps_free
    cdef pub dict temps_used_type
    cdef pub set zombie_temps
    cdef pub size_t temp_counter
    cdef pub list collect_temps_stack

    cdef pub object closure_temps
    cdef pub bint should_declare_error_indicator
    cdef pub bint uses_error_indicator
    cdef pub bint error_without_exception

    cdef pub bint needs_refnanny

    @cython.locals(n=size_t)
    cpdef new_label(self, name=*)
    cpdef tuple get_loop_labels(self)
    cpdef set_loop_labels(self, labels)
    cpdef tuple get_all_labels(self)
    cpdef set_all_labels(self, labels)
    cpdef start_collecting_temps(self)
    cpdef stop_collecting_temps(self)

    cpdef list temps_in_use(self)

cdef class IntConst:
    cdef pub object cname
    cdef pub object value
    cdef pub bint is_long

cdef class PyObjectConst:
    cdef pub object cname
    cdef pub object type

cdef class StringConst:
    cdef pub object cname
    cdef pub object text
    cdef pub object escaped_value
    cdef pub dict py_strings
    cdef pub list py_versions

    @cython.locals(intern=bint, is_str=bint, is_unicode=bint)
    cpdef get_py_string_const(self, encoding, identifier=*, is_str=*, py3str_cstring=*)

## cdef class PyStringConst:
##     cdef pub object cname
##     cdef pub object encoding
##     cdef pub bint is_str
##     cdef pub bint is_unicode
##     cdef pub bint intern

#class GlobalState(object):

#def funccontext_property(name):

cdef class CCodeWriter(object):
    cdef readonly StringIOTree buffer
    cdef readonly list pyclass_stack
    cdef readonly object globalstate
    cdef readonly object funcstate
    cdef object code_config
    cdef object last_pos
    cdef object last_marked_pos
    cdef isize level
    cdef pub isize call_level  # debug-only, see Nodes.py
    cdef bint bol

    cpdef write(self, s)
    @cython.final
    cdef _write_lines(self, s)
    cpdef _write_to_buffer(self, s)
    cpdef put(self, code)
    cpdef put_safe(self, code)
    cpdef putln(self, code=*, bint safe=*)
    @cython.final
    cdef increase_indent(self)
    @cython.final
    cdef decrease_indent(self)
    @cython.final
    cdef indent(self)

cdef class PyrexCodeWriter:
    cdef pub object f
    cdef pub isize level
