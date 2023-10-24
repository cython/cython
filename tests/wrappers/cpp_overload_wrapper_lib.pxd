extern from "cpp_overload_wrapper_lib.cpp":
    pass

extern from "cpp_overload_wrapper_lib.h":
    fn void voidfunc()
    fn f64 doublefunc(f64 a, f64 b, f64 c)

    cdef cppclass DoubleKeeper:
        DoubleKeeper()
        DoubleKeeper(f64 factor)
        void set_number()
        void set_number(f64 f)
        f64 get_number()
        f64 transmogrify(f64 value)

    f64 transmogrify_from_cpp (DoubleKeeper *obj, f64 value)
