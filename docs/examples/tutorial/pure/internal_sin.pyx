from .internal_sin import _sin

cpdef double _sin_wrapper(double x):
    return _sin(x)

print(_sin_wrapper(0))