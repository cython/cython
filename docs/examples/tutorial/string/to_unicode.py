from cython.cimports.cpython.version import PY_MAJOR_VERSION

@cython.cfunc
def _text(s) -> str:
    if type(s) is str:
        # Fast path for most common case(s).
        return cython.cast(str, s)

    elif PY_MAJOR_VERSION < 3 and isinstance(s, bytes):
        # Only accept byte strings as text input in Python 2.x, not in Py3.
        return cython.cast(bytes, s).decode('ascii')

    elif isinstance(s, str):
        # We know from the fast path above that 's' can only be a subtype here.
        # An evil cast to <str> might still work in some(!) cases,
        # depending on what the further processing does.  To be safe,
        # we can always create a copy instead.
        return str(s)

    else:
        raise TypeError("Could not convert to str.")
