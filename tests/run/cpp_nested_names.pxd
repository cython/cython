# cython: language_level=3

from libcpp.string cimport string

cdef extern from "cpp_nested_names_helper.h":
    cdef cppclass Outer:
        cppclass Nested:
            cppclass NestedNested:
                string get_str()

            string get_str()

            @staticmethod
            NestedNested get()

        @staticmethod
        Nested get()
