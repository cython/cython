# distutils: language = c++

cdef extern from "<algorithm>" namespace "std":
    T max[T](T a, T b)

print(max[long](3, 4))
print(max(1.5, 2.5))  # simple template argument deduction
