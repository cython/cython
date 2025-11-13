typeof = getattr(cython, "typeof")
cython.declare(n=cython.longlong)
print(typeof(n))
