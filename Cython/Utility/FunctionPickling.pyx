########################## function_pickling ############################

cdef extern from *:
    void* PyLong_AsVoidPtr(object)
    # implementation function - implemented in C
    object __pyx_unpickle_cyfunction_pointer_implementation(object)

{{for cname in cnames}}
    void *{{cname}}  # tell Cython that all cnames are an extern void pointer
{{endfor}}

def __pyx_lookup_cyfunction_pointer(ptr_as_pyint):
    cdef void *ptr = PyLong_AsVoidPtr(ptr_as_pyint)
{{for cname in cnames}}
    if ptr == {{cname}}:
        return u"{{cname}}"
{{endfor}}
    raise ValueError()  # __reduce__ ignores this anyway

def __pyx_unpickle_cyfunction_pointer(*args):
    return __pyx_unpickle_cyfunction_pointer_implementation(args)
