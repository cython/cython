############### ExceptStar ##########################
# I'd really like to use _PyxExc_PrepReraiseStar but it isn't exported publicly
# so reimplement it here in Cython

cdef extern from *:
    # All these functions can return NULL as a valid outcome, therefore wrap them
    # in something that returns a dummy object in this case
    """
    static PyObject *__Pyx_Safe_PyException_GetTraceback(PyObject *exc, PyObject *dummy_null) {
        PyObject *out = PyException_GetTraceback(exc);
        if (out) return out;
        if (PyErr_Occurred()) return NULL;
        return Py_NewRef(dummy_null);
    }

    static PyObject *__Pyx_Safe_PyException_GetCause(PyObject *exc, PyObject *dummy_null) {
        PyObject *out = PyException_GetCause(exc);
        if (out) return out;
        if (PyErr_Occurred()) return NULL;
        return Py_NewRef(dummy_null);
    }

    static PyObject *__Pyx_Safe_PyException_GetContext(PyObject *exc, PyObject *dummy_null) {
        PyObject *out = PyException_GetContext(exc);
        if (out) return out;
        if (PyErr_Occurred()) return NULL;
        return Py_NewRef(dummy_null);
    }
    """
    object __Pyx_Safe_PyException_GetTraceback(object, object)
    object __Pyx_Safe_PyException_GetCause(object, object)
    object __Pyx_Safe_PyException_GetContext(object, object)

@cname("__Pyx_exception_get_notes")
cdef get_notes(exc, dummy_null):
    # Not all exceptions have notes
    if hasattr(exc, "__notes__"):
        return exc.__notes__
    else:
        return dummy_null  # dummy object will always pass the "is" test

@cname("__Pyx_split_into_same_metadata")
cdef split_into_same_metadata(original, list exceptions):
    # returns a list with the same cause and a list with different causes
    cdef list same = []
    cdef list different = []

    dummy_null = object()

    original_notes = get_notes(original, dummy_null)
    original_traceback = __Pyx_Safe_PyException_GetTraceback(original, dummy_null)
    original_cause = __Pyx_Safe_PyException_GetCause(original, dummy_null)
    original_context = __Pyx_Safe_PyException_GetContext(original, dummy_null)

    for e in exceptions:
        if e is None:
            continue
        if (get_notes(e, dummy_null) is original_notes and
                __Pyx_Safe_PyException_GetTraceback(e, dummy_null) is original_traceback and
                __Pyx_Safe_PyException_GetCause(e, dummy_null) is original_cause and
                __Pyx_Safe_PyException_GetContext(e, dummy_null) is original_context):
            same.append(e)
        else:
            different.append(e)

    return same, different

@cname("__Pyx_except_star_leafs")
cdef get_leafs(keep):
    # get a set with ids of all the leafs
    cdef list to_process = list(keep)
    cdef set leafs = set()
    for e_or_eg in to_process:
        if not isinstance(e_or_eg, BaseExceptionGroup):
            leafs.add(id(e_or_eg))
        else:
            to_process.extend(e_or_eg.exceptions)
    return leafs

@cname("__Pyx_exception_group_projection")
cdef exception_group_projection(orig, keep):
    leafs = get_leafs(keep)

    # BaseExceptionGroup.split requires an actual Python function - a Cython callable won't do
    func = eval("lambda x: id(x) in leafs", {'leafs': leafs})
    return orig.split(func)[0]

@cname("__Pyx__PyExc_PrepReraiseStar")
cdef prep_reraise_star(orig, excs):
    cdef list reraised, raised
    if not excs:
        return None
    if not isinstance(orig, BaseExceptionGroup):
        assert len(excs) == 1 or len(excs) == 2 and excs[1] is None
        return excs[0]
    reraised, raised = split_into_same_metadata(orig, excs)
    reraised_eg = exception_group_projection(orig, reraised)
    if not raised:
        return reraised_eg
    if reraised_eg is not None:
        raised.append(reraised_eg)
    if len(raised) > 1:
        return BaseExceptionGroup("", raised)
    return raised[0]
