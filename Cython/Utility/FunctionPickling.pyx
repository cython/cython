########################## function_pickling ############################
#@substitute: naming

cdef extern from *:
    void* PyLong_AsVoidPtr(object)
    # implementation function - implemented in C
    object $cyfunction_unpickle_impl_cname(object)

{{for cname in cnames}}
    void *{{cname}}  # tell Cython that all cnames are an extern void pointer
{{endfor}}

def $cyfunction_pickle_lookup_ptr(ptr_as_pyint):
    cdef void *ptr = PyLong_AsVoidPtr(ptr_as_pyint)
{{for cname in cnames}}
    if ptr == {{cname}}:
        return u"{{cname}}"
{{endfor}}
    raise ValueError()  # __reduce__ ignores this anyway

def $cyfunction_unpickle_name(*args):
    return $cyfunction_unpickle_impl_cname(args)
