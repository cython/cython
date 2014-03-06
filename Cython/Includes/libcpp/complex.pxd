# Note: I might have missed some integer versions of the functions

cdef extern from "<complex>" namespace "std":
    cdef cppclass complex[T]:
        complex() nogil except +
        complex(T, T) nogil except +
        complex(complex[T]&) nogil except +
        # How to make the converting constructor, i.e. convert complex[double]
        # to complex[float]?

        complex[T] operator+(complex[T]&) nogil
        complex[T] operator-(complex[T]&) nogil
        complex[T] operator+(complex[T]&, complex[T]&) nogil
        complex[T] operator+(complex[T]&, T&) nogil
        complex[T] operator+(T&, complex[T]&) nogil
        complex[T] operator-(complex[T]&, complex[T]&) nogil
        complex[T] operator-(complex[T]&, T&) nogil
        complex[T] operator-(T&, complex[T]&) nogil
        complex[T] operator*(complex[T]&, complex[T]&) nogil
        complex[T] operator*(complex[T]&, T&) nogil
        complex[T] operator*(T&, complex[T]&) nogil
        complex[T] operator/(complex[T]&, complex[T]&) nogil
        complex[T] operator/(complex[T]&, T&) nogil
        complex[T] operator/(T&, complex[T]&) nogil

        bint operator==(complex[T]&, complex[T]&) nogil
        bint operator==(complex[T]&, T&) nogil
        bint operator==(T&, complex[T]&) nogil
        bint operator!=(complex[T]&, complex[T]&) nogil
        bint operator!=(complex[T]&, T&) nogil
        bint operator!=(T&, complex[T]&) nogil

        # Return real part
        T real(complex[T]&) nogil
        long double real(long double) nogil
        double real(double) nogil
        float real(float) nogil

        # Access real part  nogil
        T real() nogil
        void real(T) nogil

        # Return imaginary part  nogil
        T imag(complex[T]&) nogil
        long double imag(long double) nogil
        double imag(double) nogil
        float imag(float) nogil

        # Access imaginary part  nogil
        T image() nogil
        void image(T) nogil

        T abs(complex[T]&) nogil
        T arg(complex[T]&) nogil
        long double arg(long double) nogil
        double arg(double) nogil
        float arg(float) nogil

        T norm(complex[T]) nogil
        long double norm(long double) nogil
        double norm(double) nogil
        float norm(float) nogil

        complex[T] conj(complex[T]&) nogil
        complex[long double] conj(long double) nogil
        complex[double] conj(double) nogil
        complex[float] conj(float) nogil

        complex[T] proj(complex[T]) nogil
        complex[long double] proj(long double) nogil
        complex[double] proj(double) nogil
        complex[float] proj(float) nogil

        complex[T] polar(T&, T&) nogil
        complex[T] ploar(T&) nogil
 
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
