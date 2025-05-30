cdef extern from *:
    int CYTHON_COMPILING_IN_LIMITED_API

def skip_if_limited_api(why, other_test=True):
    def dec(f):
        if CYTHON_COMPILING_IN_LIMITED_API and other_test:
            return None
        else:
            return f

    return dec
