cdef extern from "cpp_overload_wrapper_lib.cpp":
    pass
cdef extern from "cpp_overload_wrapper_lib.h":
    void voidfunc()
    double doublefunc(double a, double b, double c)

    cdef cppclass DoubleKeeper:
        DoubleKeeper()
        DoubleKeeper(double factor)
        void set_number()
        void set_number(double f)
        double get_number()
        double transmogrify(double value)

    double transmogrify_from_cpp (DoubleKeeper *obj, double value)
