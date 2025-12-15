import cython
obj = 123
i1 = cython.cast(cython.int, obj)
i2 = cython.cast(cython.int, obj, typecheck=True)
