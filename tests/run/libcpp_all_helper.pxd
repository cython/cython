from libcpp.unordered_map cimport unordered_map

cdef extern from "libcpp_all_helper.h":
    cdef cppclass MyStruct:
        pass

    cdef cppclass Hasher:
        pass

    cdef unordered_map[MyStruct, int] map_with_specific_hasher
