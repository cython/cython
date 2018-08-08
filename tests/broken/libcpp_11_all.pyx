# tag: cpp

cimport libcpp
cimport libcpp.pair
cimport libcpp.unordered_map

from libcpp.unordered_map cimport *

cdef libcpp.unordered_map.unordered_map[int,int] um1 = unordered_map[int,int]()
cdef libcpp.pair.pair[int,int] p1 = pair[int,int](1,2)

cdef unordered_map[int,int].iterator ium1 = um1.begin()
cdef unordered_map[int,int].iterator ium2 = um1.end()
cdef pair[unordered_map[int,int].iterator, bint] piumb = um1.insert(p1)
cdef unordered_map[int,int].iterator ium3 = um1.begin()
cdef unordered_map[int,int].iterator ium4 = um1.erase(ium3)
