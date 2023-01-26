# cython: language_level=3

from libcpp.string cimport string

cdef extern from "cpp_nested_names_helper.h":
    cdef cppclass A:
        cppclass B:
            string get_str()

        @staticmethod
        B get()
