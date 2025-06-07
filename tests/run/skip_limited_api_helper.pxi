cdef extern from *:
    int CYTHON_COMPILING_IN_LIMITED_API

def skip_if_limited_api(why, *, min_runtime_version=None):
    import sys
    def dec(f):
        if (CYTHON_COMPILING_IN_LIMITED_API and
                (min_runtime_version is None or sys.version_info < min_runtime_version)):
            return None
        else:
            return f

    return dec
