extern from "cpp_overload_wrapper_lib.cpp":
    pass

extern from "cpp_overload_wrapper_lib.h":
    void voidfunc()
    f64 doublefunc(f64 a, f64 b, f64 c)

    cdef cppclass DoubleKeeper:
        DoubleKeeper()
        DoubleKeeper(f64 factor)
        void set_number()
        void set_number(double f)
        double get_number()
        double transmogrify(f64 value)

    f64 transmogrify_from_cpp (DoubleKeeper *obj, f64 value)
