########################## function_pickling ############################

cdef extern from *:
    void* PyLong_AsVoidPtr(object)

{{for cname in cnames}}
    void *{{cname}}  # tell Cython that all cnames are an extern void pointer
{{endfor}}

def __pyx_lookup_cyfunction_pointer(ptr_as_pyint):
    cdef void *ptr = PyLong_AsVoidPtr(ptr_as_pyint)
{{for cname in cnames}}
    if ptr == {{cname}}:
        return "{{cname}}"
{{endfor}}
    raise ValueError()  # __reduce__ ignores this anyway

# TODO reverse function
