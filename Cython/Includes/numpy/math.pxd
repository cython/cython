# NumPy math library
#
# This exports the functionality of the NumPy core math library, aka npymath,
# which provides implementations of C99 math functions and macros for system
# with a C89 library (such as MSVC). npymath is available with NumPy >=1.3,
# although some functions will require later versions. The spacing function is
# not in C99, but comes from Fortran.
#
# On the Cython side, the npymath functions are available without the "npy_"
# prefix that they have in C, to make this is a drop-in replacement for
# libc.math. The same is true for the constants, where possible.
#
# See the NumPy documentation for linking instructions.
#
# Complex number support and NumPy 2.0 half-precision functions are currently
# not exported.
#
# Author: Lars Buitinck

cdef extern from "numpy/npy_math.h" nogil:
    # Floating-point classification
    long double NAN "NPY_NAN"
    long double INFINITY "NPY_INFINITY"
    long double PZERO "NPY_PZERO"        # positive zero
    long double NZERO "NPY_NZERO"        # negative zero

    # These four are actually macros and work on any floating-point type.
    bint isfinite "npy_isfinite"(long double)
    bint isinf "npy_isinf"(long double)
    bint isnan "npy_isnan"(long double)
    bint signbit "npy_signbit"(long double)

    double copysign "npy_copysign"(double, double)

    # Math constants
    long double E "NPY_E"
    long double LOG2E "NPY_LOG2E"       # ln(e) / ln(2)
    long double LOG10E "NPY_LOG10E"     # ln(e) / ln(10)
    long double LOGE2 "NPY_LOGE2"       # ln(2)
    long double LOGE10 "NPY_LOGE10"     # ln(10)
    long double PI "NPY_PI"
    long double PI_2 "NPY_PI_2"         # pi / 2
    long double PI_4 "NPY_PI_4"         # pi / 4
    long double NPY_1_PI                # 1 / pi; NPY_ because of ident syntax
    long double NPY_2_PI                # 2 / pi
    long double EULER "NPY_EULER"       # Euler constant (gamma, 0.57721)

    # Low-level floating point manipulation (NumPy >=1.4)
    double nextafter "npy_nextafter"(double x, double y)
    double spacing "npy_spacing"(double x)
