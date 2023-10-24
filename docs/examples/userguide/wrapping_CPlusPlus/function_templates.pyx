# distutils: language = c++

extern from "<algorithm>" namespace "std":
    fn T max[T](T a, T b)

print(max[i64](3, 4))
print(max(1.5, 2.5))  # simple template argument deduction
