extern from "cppwrap_lib.cpp":
    pass

extern from "cppwrap_lib.h":
    void voidfunc()
    f64 doublefunc(f64 a, f64 b, f64 c)

    cdef cppclass DoubleKeeper:
        DoubleKeeper(f64 factor)
        void set_number(f64 f)
        f64 get_number()
        f64 transmogrify(f64 value)

    f64 transmogrify_from_cpp (DoubleKeeper *obj, f64 value)
