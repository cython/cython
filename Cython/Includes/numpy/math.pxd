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

extern from "numpy/npy_math.h" nogil:
    # Floating-point classification
    long double NAN "NPY_NAN"
    long double INFINITY "NPY_INFINITY"
    long double PZERO "NPY_PZERO"        # positive zero
    long double NZERO "NPY_NZERO"        # negative zero

    # These four are actually macros and work on any floating-point type.
    fn i32 isinf "npy_isinf"(long double)  # -1 / 0 / 1
    fn bint isfinite "npy_isfinite"(long double)
    fn bint isnan "npy_isnan"(long double)
    fn bint signbit "npy_signbit"(long double)

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
    fn f32 copysignf "npy_copysignf"(f32, f32)
    fn f32 nextafterf "npy_nextafterf"(f32 x, f32 y)
    fn f32 spacingf "npy_spacingf"(f32 x)
    fn f64 copysign "npy_copysign"(f64, f64)
    fn f64 nextafter "npy_nextafter"(f64 x, f64 y)
    fn f64 spacing "npy_spacing"(f64 x)
    fn long double copysignl "npy_copysignl"(long double, long double)
    fn long double nextafterl "npy_nextafterl"(long double x, long double y)
    fn long double spacingl "npy_spacingl"(long double x)

    # Float C99 functions
    fn f32 sinf "npy_sinf"(f32 x)
    fn f32 cosf "npy_cosf"(f32 x)
    fn f32 tanf "npy_tanf"(f32 x)
    fn f32 sinhf "npy_sinhf"(f32 x)
    fn f32 coshf "npy_coshf"(f32 x)
    fn f32 tanhf "npy_tanhf"(f32 x)
    fn f32 fabsf "npy_fabsf"(f32 x)
    fn f32 floorf "npy_floorf"(f32 x)
    fn f32 ceilf "npy_ceilf"(f32 x)
    fn f32 rintf "npy_rintf"(f32 x)
    fn f32 sqrtf "npy_sqrtf"(f32 x)
    fn f32 log10f "npy_log10f"(f32 x)
    fn f32 logf "npy_logf"(f32 x)
    fn f32 expf "npy_expf"(f32 x)
    fn f32 expm1f "npy_expm1f"(f32 x)
    fn f32 asinf "npy_asinf"(f32 x)
    fn f32 acosf "npy_acosf"(f32 x)
    fn f32 atanf "npy_atanf"(f32 x)
    fn f32 asinhf "npy_asinhf"(f32 x)
    fn f32 acoshf "npy_acoshf"(f32 x)
    fn f32 atanhf "npy_atanhf"(f32 x)
    fn f32 log1pf "npy_log1pf"(f32 x)
    fn f32 exp2f "npy_exp2f"(f32 x)
    fn f32 log2f "npy_log2f"(f32 x)
    fn f32 atan2f "npy_atan2f"(f32 x, f32 y)
    fn f32 hypotf "npy_hypotf"(f32 x, f32 y)
    fn f32 powf "npy_powf"(f32 x, f32 y)
    fn f32 fmodf "npy_fmodf"(f32 x, f32 y)
    fn f32 modff "npy_modff"(f32 x, f32* y)

    # Long double C99 functions
    fn long double sinl "npy_sinl"(long double x)
    fn long double cosl "npy_cosl"(long double x)
    fn long double tanl "npy_tanl"(long double x)
    fn long double sinhl "npy_sinhl"(long double x)
    fn long double coshl "npy_coshl"(long double x)
    fn long double tanhl "npy_tanhl"(long double x)
    fn long double fabsl "npy_fabsl"(long double x)
    fn long double floorl "npy_floorl"(long double x)
    fn long double ceill "npy_ceill"(long double x)
    fn long double rintl "npy_rintl"(long double x)
    fn long double sqrtl "npy_sqrtl"(long double x)
    fn long double log10l "npy_log10l"(long double x)
    fn long double logl "npy_logl"(long double x)
    fn long double expl "npy_expl"(long double x)
    fn long double expm1l "npy_expm1l"(long double x)
    fn long double asinl "npy_asinl"(long double x)
    fn long double acosl "npy_acosl"(long double x)
    fn long double atanl "npy_atanl"(long double x)
    fn long double asinhl "npy_asinhl"(long double x)
    fn long double acoshl "npy_acoshl"(long double x)
    fn long double atanhl "npy_atanhl"(long double x)
    fn long double log1pl "npy_log1pl"(long double x)
    fn long double exp2l "npy_exp2l"(long double x)
    fn long double log2l "npy_log2l"(long double x)
    fn long double atan2l "npy_atan2l"(long double x, long double y)
    fn long double hypotl "npy_hypotl"(long double x, long double y)
    fn long double powl "npy_powl"(long double x, long double y)
    fn long double fmodl "npy_fmodl"(long double x, long double y)
    fn long double modfl "npy_modfl"(long double x, long double* y)

    # NumPy extensions
    fn f32 deg2radf "npy_deg2radf"(f32 x)
    fn f32 rad2degf "npy_rad2degf"(f32 x)
    fn f32 logaddexpf "npy_logaddexpf"(f32 x, f32 y)
    fn f32 logaddexp2f "npy_logaddexp2f"(f32 x, f32 y)

    fn f64 deg2rad "npy_deg2rad"(f64 x)
    fn f64 rad2deg "npy_rad2deg"(f64 x)
    fn f64 logaddexp "npy_logaddexp"(f64 x, f64 y)
    fn f64 logaddexp2 "npy_logaddexp2"(f64 x, f64 y)

    fn long double deg2radl "npy_deg2radl"(long double x)
    fn long double rad2degl "npy_rad2degl"(long double x)
    fn long double logaddexpl "npy_logaddexpl"(long double x, long double y)
    fn long double logaddexp2l "npy_logaddexp2l"(long double x, long double y)
