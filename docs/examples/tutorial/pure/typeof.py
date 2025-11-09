typeof = getattr(cython, "typeof", type)
cython.declare(n=cython.longlong)
print(typeof(n))