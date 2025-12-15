import cython
# typeof() is a compile-time-only feature and is not available in pure Python.
# This shows the untyped runtime equivalent.
cython.declare(n=cython.longlong)
n = 0
print(type(n))
