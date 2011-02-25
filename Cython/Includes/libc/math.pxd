cdef extern from "math.h" nogil:

    enum: M_E
    enum: M_LOG2E
    enum: M_LOG10E
    enum: M_LN2
    enum: M_LN10
    enum: M_PI
    enum: M_PI_2
    enum: M_PI_4
    enum: M_1_PI
    enum: M_2_PI
    enum: M_2_SQRTPI
    enum: M_SQRT2
    enum: M_SQRT1_2

    double acos(double x)
    double asin(double x)
    double atan(double x)
    double atan2(double y, double x)
    double cos(double x)
    double sin(double x)
    double tan(double x)

    double cosh(double x)
    double sinh(double x)
    double tanh(double x)
    double acosh(double x)
    double asinh(double x)
    double atanh(double x)

    double hypot(double x, double y)

    double exp(double x)
    double exp2(double x)
    double expm1(double x)
    double log(double x)
    double logb(double x)
    double log2(double x)
    double log10(double x)
    double log1p(double x)
    int ilogb(double x)

    double lgamma(double x)
    double tgamma(double x)

    double frexp(double x, double* exponent)
    double ldexp(double x, double exponent)

    double modf(double x, double* iptr)
    double fmod(double x, double y)
    double remainder(double x, double y)
    double remquo(double x, double y, int *quot)
    double pow(double x, double y)
    double sqrt(double x)
    double cbrt(double x)

    double fabs(double x)
    double ceil(double x)
    double floor(double x)
    double trunc(double x)
    double rint(double x)
    double round(double x)
    double nearbyint(double x)
    double nextafter(double, double)
    double nexttoward(double, long double)

    long long llrint(double)
    long lrint(double)
    long long llround(double)
    long lround(double)

    double copysign(double, double)
    double erf(double)
    double erfc(double)

    double fdim(double x, double y)
    double fma(double x, double y)
    double fmax(double x, double y)
    double fmin(double x, double y)
    double scalbln(double x, long n)
    double scalbn(double x, int n)

    double nan(char*) # const char*
    
