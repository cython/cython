########################## function_pickling ############################
#@substitute: naming
#@merge_at_end: True

cdef extern from *:
    ctypedef void (*__Pyx_generic_func_pointer)()
    __Pyx_generic_func_pointer __Pyx_capsule_to_c_func_ptr(object, const char*) except NULL
    # implementation function - implemented in C
    object $cyfunction_unpickle_impl_cname(int, object, object, object, object)

{{for cname in cnames}}
    void *{{cname}}  # tell Cython that all cnames are an extern void pointer
{{endfor}}

def $cyfunction_pickle_lookup_ptr(ptr_as_pyint):
    cdef __Pyx_generic_func_pointer ptr = __Pyx_capsule_to_c_func_ptr(ptr_as_pyint, "CyFunc capsule")
{{for cname in cnames}}
    if ptr == <__Pyx_generic_func_pointer>{{cname}}:
        return b"{{cname}}"
{{endfor}}
    raise ValueError()  # __reduce__ ignores this anyway

cdef str cyfunc_pickle_err = \
"""Unpickling of CyFunction failed. This may be a bug or it may be:
    1. You used have rebuilt your module with a different version of Cython since pickling;
    2. You have changed your own module since pickling.
Cython does not attempt to keep compatibility in these cases.
"""

# Lots of string comparisons in $cyfunction_unpickle_impl_cname are probably slow because
# it has to do a character-by-character comparison of "key" with many different string names.
# I'm hoping that dict lookups of bytes objects are fairly optimized, and C switches
# can be well optimized. Thus the lookup in two stages: dict lookup to index, index as
# switch
cdef dict lookup_table = {
{{for cname in cnames}}
    b"{{cname}}": {{cnames_to_index[cname]}},
{{endfor}}
}

def $cyfunction_unpickle_name(key, reduced_closure, defaults_tuple, defaults_kwdict):
    try:
        keyindex = lookup_table.get(key)
        if keyindex is None:
            raise ValueError(f"Could not match key \'{key.decode()}\' when unpickling CyFunction")
        return $cyfunction_unpickle_impl_cname(<int>keyindex, key, reduced_closure, defaults_tuple, defaults_kwdict)
    except BaseException as e:
        try:
            from pickle import UnpicklingError
        except:
            raise e  # I'd like to give a better error message, but if it fails just provide the original
        else:
            # provide a detailed message to set user expectations
            raise UnpicklingError(cyfunc_pickle_err) from e
