
cdef str _text(s):
    if type(s) is str:
        # Fast path for most common case(s).
        return <str>s

    elif isinstance(s, str):
        # We know from the fast path above that 's' can only be a subtype here.
        # An evil cast to <str> might still work in some(!) cases,
        # depending on what the further processing does.  To be safe,
        # we can always create a copy instead.
        return str(s)

    else:
        raise TypeError("Could not convert to str.")
