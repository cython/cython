from .mymodule import sin

cpdef double sin_wrapper(double x):
    return sin(x)

print(sin_wrapper(0))