cdef extern from "cppwrap_lib.cpp":
    pass
cdef extern from "cppwrap_lib.h":
    void voidfunc()
    double doublefunc(double a, double b, double c)

    cdef cppclass DoubleKeeper:
        DoubleKeeper(double factor)
        void set_number(double f)
        double get_number()
        double transmogrify(double value)

    double transmogrify_from_cpp (DoubleKeeper *obj, double value)
