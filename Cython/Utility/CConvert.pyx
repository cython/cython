#################### FromPyStructUtility ####################

cdef extern from *:
    ctypedef struct PyTypeObject:
        char* tp_name
    PyTypeObject *Py_TYPE(obj)
    bint PyMapping_Check(obj)
    object PyErr_Format(exc, const char *format, ...)
    int __Pyx_RaiseUnexpectedTypeError(const char *expected, object obj) except 0

@cname("{{funcname}}")
cdef {{struct_type}} {{funcname}}(obj) except *:
    cdef {{struct_type}} result
    if not PyMapping_Check(obj):
        __Pyx_RaiseUnexpectedTypeError(b"a mapping", obj)

    {{for member in var_entries:}}
    try:
        value = obj['{{member.name}}']
    except KeyError:
        raise ValueError("No value specified for struct attribute '{{member.name}}'")
    result.{{member.name}} = value
    {{endfor}}
    return result


#################### FromPyUnionUtility ####################

cdef extern from *:
    ctypedef struct PyTypeObject:
        char* tp_name
    PyTypeObject *Py_TYPE(obj)
    bint PyMapping_Check(obj)
    object PyErr_Format(exc, const char *format, ...)
    int __Pyx_RaiseUnexpectedTypeError(const char *expected, object obj) except 0

@cname("{{funcname}}")
cdef {{struct_type}} {{funcname}}(obj) except *:
    cdef {{struct_type}} result
    cdef Py_ssize_t length
    if not PyMapping_Check(obj):
        __Pyx_RaiseUnexpectedTypeError(b"a mapping", obj)

    last_found = None
    length = len(obj)
    if length:
        {{for member in var_entries:}}
        if '{{member.name}}' in obj:
            if last_found is not None:
                raise ValueError("More than one union attribute passed: '%s' and '%s'" % (last_found, '{{member.name}}'))
            last_found = '{{member.name}}'
            result.{{member.cname}} = obj['{{member.name}}']
            length -= 1
            if not length:
                return result
        {{endfor}}
    if last_found is None:
        raise ValueError("No value specified for any of the union attributes (%s)" %
                         '{{", ".join(member.name for member in var_entries)}}')
    return result


#################### cfunc.to_py ####################

@cname("{{cname}}")
cdef object {{cname}}({{return_type.ctype}} (*f)({{ ', '.join(arg.type_cname for arg in args) }}) {{except_clause}}):
    def wrap({{ ', '.join('{arg.ctype} {arg.name}'.format(arg=arg) for arg in args) }}):
        """wrap({{', '.join(('{arg.name}: {arg.type_displayname}'.format(arg=arg) if arg.type_displayname else arg.name) for arg in args)}}){{if return_type.type_displayname}} -> {{return_type.type_displayname}}{{endif}}"""
        {{'' if return_type.type.is_void else 'return '}}f({{ ', '.join(arg.name for arg in args) }})
    return wrap


#################### carray.from_py ####################

cdef extern from *:
    object PyErr_Format(exc, const char *format, ...)

@cname("{{cname}}")
cdef int {{cname}}(object o, {{base_type}} *v, Py_ssize_t length) except -1:
    cdef Py_ssize_t i = length
    try:
        i = len(o)
    except (TypeError, OverflowError):
        pass
    if i == length:
        for i, item in enumerate(o):
            if i >= length:
                break
            v[i] = item
        else:
            i += 1  # convert index to length
            if i == length:
                return 0

    PyErr_Format(
        IndexError,
        ("too many values found during array assignment, expected %zd"
         if i >= length else
         "not enough values found during array assignment, expected %zd, got %zd"),
        length, i)


#################### carray.to_py ####################

cdef extern from *:
    void Py_INCREF(object o)
    tuple PyTuple_New(Py_ssize_t size)
    list PyList_New(Py_ssize_t size)
    void PyTuple_SET_ITEM(object  p, Py_ssize_t pos, object o)
    void PyList_SET_ITEM(object  p, Py_ssize_t pos, object o)


@cname("{{cname}}")
cdef inline list {{cname}}({{base_type}} *v, Py_ssize_t length):
    cdef size_t i
    cdef object value
    l = PyList_New(length)
    for i in range(<size_t>length):
        value = v[i]
        Py_INCREF(value)
        PyList_SET_ITEM(l, i, value)
    return l


@cname("{{to_tuple_cname}}")
cdef inline tuple {{to_tuple_cname}}({{base_type}} *v, Py_ssize_t length):
    cdef size_t i
    cdef object value
    t = PyTuple_New(length)
    for i in range(<size_t>length):
        value = v[i]
        Py_INCREF(value)
        PyTuple_SET_ITEM(t, i, value)
    return t

#################### c_array_slice.to_py ####################

cdef extern from *:
    void Py_INCREF(object o)
    void Py_DECREF(object o)
    object PyErr_Format(exc, const char *format, ...)

    list PyList_New(Py_ssize_t size)
    void PyList_SET_ITEM(object p, Py_ssize_t pos, object o)

    tuple PyTuple_New(Py_ssize_t size)
    void PyTuple_SET_ITEM(object p, Py_ssize_t pos, object o)

    frozenset __Pyx_PyFrozenSet_New(object)
    set PySet_New(void *)
    int PySet_Add(object p, object o) except -1

@cname("{{cname}}")
cdef inline {{to_py_obj_type}} {{cname}}({{base_type}} *arr, Py_ssize_t arr_size, Py_ssize_t from_idx, Py_ssize_t to_idx, int wraparound, int boundscheck):
    cdef Py_ssize_t i, length = 0

    if wraparound:
        if from_idx < 0:
            from_idx += arr_size

        if to_idx < 0:
            to_idx += arr_size

    if boundscheck:
        if from_idx >= to_idx:
             from_idx = to_idx = 0
        else:
            if from_idx < 0:
                from_idx = 0

            if to_idx > arr_size:
                to_idx = arr_size

    length = to_idx - from_idx

    {{if to_py_obj_type == 'list'}}
    container = PyList_New(length)
    {{elif to_py_obj_type == 'tuple'}}
    container = PyTuple_New(length)

    # The PySet_New is used for creating frozenset,
    # since PyFrozenSet_New has a bug with PySet_Add in PyPy.
    #
    # __Pyx_PyFrozenSet_New(NULL) doesn't work for this goal,
    # since it returns immutable frozenset-singleton.
    {{elif to_py_obj_type == 'set' or to_py_obj_type == 'frozenset'}}
    container = PySet_New(NULL)
    {{else}}
        {{py: assert False, "Invalid target type for C array conversion: %r" % to_py_obj_type}}
    {{endif}}


    cdef object value
    if length > 0:
        for i in range(from_idx, to_idx):
            value = arr[i]

            {{if to_py_obj_type == 'list'}}
            Py_INCREF(value)
            PyList_SET_ITEM(container, i - from_idx, value)
            {{elif to_py_obj_type == 'tuple'}}
            Py_INCREF(value)
            PyTuple_SET_ITEM(container, i - from_idx, value)
            {{elif to_py_obj_type == 'set' or to_py_obj_type == 'frozenset'}}
            PySet_Add(container, value)
            {{endif}}

    {{if to_py_obj_type == 'frozenset'}}
    # workaround for bug with frozenset in PyPy
    container = __Pyx_PyFrozenSet_New(container)
    {{endif}}

    return container
