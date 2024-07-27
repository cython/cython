from libcpp.functional cimport function

cdef extern from "cpp_function_lib.cpp":
    # CPP is include here so that it doesn't need to be compiled externally
    pass

cdef extern from "cpp_function_lib.h":
    double add_one(double, int)
    double add_two(double a, int b)

    cdef cppclass AddAnotherFunctor:
        AddAnotherFunctor(double to_add)
        double call "operator()"(double a, int b)

    cdef cppclass FunctionKeeper:
        FunctionKeeper(function[double(double, int) noexcept] user_function)
        void set_function(function[double(double, int) noexcept] user_function)
        function[double(double, int) noexcept] get_function()
        double call_function(double a, int b) except +
