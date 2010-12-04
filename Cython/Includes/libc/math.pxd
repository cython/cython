cdef extern from "math.h":

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

    double exp(double x)
    double log(double x)
    double log10(double x)

    double pow(double x, double y)
    double sqrt(double x)
