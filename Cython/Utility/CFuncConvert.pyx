#################### cfunc.to_py ####################

cdef extern from *:
    ctypedef struct PyObject
    ctypedef struct PyTypeObject
    cdef bint __Pyx_TypeTest(PyObject*, PyTypeObject* type) except 0
  {{for arg in args}}
    {{arg.declare_type_def()}}
    {{arg.declare_type_convert()}}
  {{endfor}}
    {{declare_return_type}}
    {{declare_return_type_convert}}

@cname("{{cname}}")
cdef object {{cname}}({{return_type}} (*f)({{ ', '.join(arg.type_name for arg in args) }}) {{except_clause}}):
    def wrap({{ ', '.join('{arg.py_arg_type} {arg.name}'.format(arg=arg) for arg in args) }}):
        """wrap({{', '.join('{arg.name}: {arg.type_displayname!r}'.format(arg=arg) for arg in args)}}){{if return_type_displayname}} -> {{repr(return_type_displayname)}}{{endif}}"""
        {{for arg in args}}
        {{arg.check_type()}}
        {{endfor}}
        {{maybe_return}}(f({{ ', '.join('%s(%s)' % (arg.type_convert, arg.name) for arg in args) }}))
    return wrap
