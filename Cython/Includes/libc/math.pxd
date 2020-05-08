cdef extern from "<math.h>" nogil:
    const double M_E
    const double e "M_E"  # as in Python's math module
    const double M_LOG2E
    const double M_LOG10E
    const double M_LN2
    const double M_LN10
    const double M_PI
    const double pi "M_PI"  # as in Python's math module
    const double M_PI_2
    const double M_PI_4
    const double M_1_PI
    const double M_2_PI
    const double M_2_SQRTPI
    const double M_SQRT2
    const double M_SQRT1_2

    # C99 constants
    const float INFINITY
    const float NAN
    # note: not providing "nan" and "inf" aliases here as nan() is a function in C
    const double HUGE_VAL
    const float HUGE_VALF
    const long double HUGE_VALL

    double acos(double x)
    double acosh(double x)
    double asin(double x)
    double asinh(double x)
    double atan(double x)
    double atan2(double y, double x)
    double atanh(double x)
    double cbrt(double x)
    double ceil(double x)
    double copysign(double, double)
    float copysignf(float, float)
    long double copysignl(long double, long double)
    double cos(double x)
    double cosh(double x)
    double erf(double)
    double erfc(double)
    float erfcf(float)
    long double erfcl(long double)
    float erff(float)
    long double erfl(long double)
    double exp(double x)
    double exp2(double x)
    double expm1(double x)
    double fabs(double x)
    double fdim(double x, double y)
    double floor(double x)
    double fma(double x, double y, double z)
    double fmax(double x, double y)
    double fmin(double x, double y)
    double fmod(double x, double y)
    double frexp(double x, int* exponent)
    double hypot(double x, double y)
    int ilogb(double x)
    double ldexp(double x, int exponent)
    double lgamma(double x)
    long long llrint(double)
    long long llround(double)
    double log(double x)
    double log10(double x)
    double log1p(double x)
    double log2(double x)
    double logb(double x)
    long lrint(double)
    long lround(double)
    double modf(double x, double* iptr)
    double nan(const char*)
    double nearbyint(double x)
    double nextafter(double, double)
    double nexttoward(double, long double)
    double pow(double x, double y)
    double remainder(double x, double y)
    double remquo(double x, double y, int* quot)
    double rint(double x)
    double round(double x)
    double scalbln(double x, long n)
    double scalbn(double x, int n)
    double sin(double x)
    double sinh(double x)
    double sqrt(double x)
    double tan(double x)
    double tanh(double x)
    double tgamma(double x)
    double trunc(double x)

    int isinf(long double)   # -1 / 0 / 1
    bint isfinite(long double)
    bint isnan(long double)
    bint isnormal(long double)
    bint signbit(long double)
    int fpclassify(long double)
    const int FP_NAN
    const int FP_INFINITE
    const int FP_ZERO
    const int FP_SUBNORMAL
    const int FP_NORMAL
