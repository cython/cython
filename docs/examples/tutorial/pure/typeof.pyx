from cython import typeof
# typeof() is a compile-time feature that reports the C-level type
# of an expression. This example shows its use in a .pyx file.

cdef long long n
print(typeof(n))
