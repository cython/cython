try:
    import cython
except ImportError:
    class _fake_cython:
        compiled = False
        def cfunc(self, func): return func
        def ccall(self, func): return func
        def __getattr__(self, type_name): return "object"

    cython = _fake_cython()
