########################## function_pickling ############################
#@substitute: naming
#@merge_at_end: True

cdef extern from *:
    void *PyLong_AsVoidPtr(object pylong) except ?NULL
    # implementation function - implemented in C
    object $cyfunction_unpickle_impl_cname(object, object, object, object)

{{for cname in cnames}}
    void *{{cname}}  # tell Cython that all cnames are an extern void pointer
{{endfor}}

cdef dict ${cyfunction_pickle_lookup_ptr}_cache = {}

def $cyfunction_pickle_lookup_ptr(ptr_as_py):
    # Cache results in a dict instead of an extended chained lookup.
    # This at least ends up O(1) the second time we look something up.
    cached = ${cyfunction_pickle_lookup_ptr}_cache.get(ptr_as_py, None)
    if cached:
        return cached
    cdef void *ptr = PyLong_AsVoidPtr(ptr_as_py)
{{for cname in cnames}}
    if ptr == <void*>{{cname}}:
        ${cyfunction_pickle_lookup_ptr}_cache[ptr_as_py] = "{{cname}}"
        return "{{cname}}"
{{endfor}}
    raise ValueError()  # __reduce__ ignores this anyway

def $cyfunction_unpickle_name(key, reduced_closure, defaults_tuple, defaults_kwdict):
    try:
        return $cyfunction_unpickle_impl_cname(key, reduced_closure, defaults_tuple, defaults_kwdict)
    except BaseException as e:
        try:
            from pickle import UnpicklingError
        except:
            raise e  # I'd like to give a better error message, but if it fails just provide the original
        else:
            # provide a detailed message to set user expectations
            cyfunc_pickle_err = \
            """Unpickling of CyFunction failed. This may be a bug or it may be:
                1. You used have rebuilt your module with a different version of Cython since pickling;
                2. You have changed your own module since pickling.
            Cython does not attempt to keep compatibility in these cases.
            """
            raise UnpicklingError(cyfunc_pickle_err) from e
