import cython

T = cython.typedef(cython.p_int)

cython.declare(t=cython.uint)

t = 12345

t1 = cython.cast(cython.size_t, cython.cast(T, t))

t2 = cython.cast(cython.size_t, cython.cast(T, t, typecheck=True))

