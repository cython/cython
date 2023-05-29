############### ExceptStar ##########################
# I'd really like to use _PyxExc_PrepReraiseStar but it isn't exported publicly
# so reimplement it here in Cython

cdef extern from *:
    object PyException_GetTraceback(object)
    object PyException_GetCause(object)
    object PyException_GetContext(object)

@cname("__Pyx_split_into_same_metadata")
cdef split_into_same_metadata(original, list exceptions):
    # returns a list with the same cause and a list with different causes
    cdef list same = []
    cdef list different = []

    # TODO - replace these with C API lookups
    original_notes = original.notes
    original_traceback = PyException_GetTraceback(original)
    original_cause = PyException_GetCause(original)
    original_context = PyException_GetContext(original)

    for e in exceptions:
        if e is None:
            continue
        if (e.notes is original_notes and
                PyException_GetTraceback(e) is original_traceback and
                PyException_GetCause(e) is original_cause and
                PyException_GetContext(e) is original_context):
            same.append(e)
        else:
            different.append(e)

    return same, different

@cname("__Pyx_except_star_leafs")
cdef get_leafs(keep):
    # get a set with all the leafs. The CPython implementation does this by ID
    # but I think it's likely to be more robust to do it by object or different
    # implementations
    cdef list to_process = list(keep)
    cdef set leafs = set()
    for e_or_eg in to_process:
        if not isinstance(e_or_eg, BaseExceptionGroup):
            leafs.add(e_or_eg)
        else:
            to_process.extend(e_or_eg.exceptions)
    return leafs

@cname("__Pyx_exception_group_projection")
cdef exception_group_projection(orig, keep):
    leafs = get_leafs(keep)

    return orig.split(lambda x: x in leafs)

@cname("__Pyx_PyExc_PrepReraiseStar")
cdef prep_reraise_star(orig, excs):
    cdef list reraised, raised
    if not excs:
        return None
    if not isinstance(excs, BaseExceptionGroup):
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
