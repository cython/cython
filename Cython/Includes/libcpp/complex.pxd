# Note: add integer versions of the functions?

cdef extern from "<complex>" namespace "std" nogil:
    cdef cppclass complex[T]:
        complex() except +
        complex(T, T) except +
        complex(complex[T]&) except +
        # How to make the converting constructor, i.e. convert complex[double]
        # to complex[float]?

        complex[T] operator+(complex[T]&)
        complex[T] operator-(complex[T]&)
        complex[T] operator+(complex[T]&, complex[T]&)
        complex[T] operator+(complex[T]&, T&)
        complex[T] operator+(T&, complex[T]&)
        complex[T] operator-(complex[T]&, complex[T]&)
        complex[T] operator-(complex[T]&, T&)
        complex[T] operator-(T&, complex[T]&)
        complex[T] operator*(complex[T]&, complex[T]&)
        complex[T] operator*(complex[T]&, T&)
        complex[T] operator*(T&, complex[T]&)
        complex[T] operator/(complex[T]&, complex[T]&)
        complex[T] operator/(complex[T]&, T&)
        complex[T] operator/(T&, complex[T]&)

        bint operator==(complex[T]&, complex[T]&)
        bint operator==(complex[T]&, T&)
        bint operator==(T&, complex[T]&)
        bint operator!=(complex[T]&, complex[T]&)
        bint operator!=(complex[T]&, T&)
        bint operator!=(T&, complex[T]&)

        # Access real part
        T real()
        void real(T)

        # Access imaginary part
        T image()
        void image(T)

    # Return real part
    T real(complex[T]&)
    long double real(long double)
    double real(double)
    float real(float)

    # Return imaginary part
    T imag(complex[T]&)
    long double imag(long double)
    double imag(double)
    float imag(float)

    T abs(complex[T]&)
    T arg(complex[T]&)
    long double arg(long double)
    double arg(double)
    float arg(float)

    T norm(complex[T])
    long double norm(long double)
    double norm(double)
    float norm(float)

    complex[T] conj(complex[T]&)
    complex[long double] conj(long double)
    complex[double] conj(double)
    complex[float] conj(float)

    complex[T] proj(complex[T])
    complex[long double] proj(long double)
    complex[double] proj(double)
    complex[float] proj(float)

    complex[T] polar(T&, T&)
    complex[T] ploar(T&)

    complex[T] exp(complex[T]&)
    complex[T] log(complex[T]&)
    complex[T] log10(complex[T]&)

    complex[T] pow(complex[T]&, complex[T]&)
    complex[T] pow(complex[T]&, T&)
    complex[T] pow(T&, complex[T]&)
    # There are some promotion versions too

    complex[T] sqrt(complex[T]&)

    complex[T] sin(complex[T]&)
    complex[T] cos(complex[T]&)
    complex[T] tan(complex[T]&)
    complex[T] asin(complex[T]&)
    complex[T] acos(complex[T]&)
    complex[T] atan(complex[T]&)

    complex[T] sinh(complex[T]&)
    complex[T] cosh(complex[T]&)
    complex[T] tanh(complex[T]&)

    complex[T] asinh(complex[T]&)
    complex[T] acosh(complex[T]&)
    complex[T] atanh(complex[T]&)
