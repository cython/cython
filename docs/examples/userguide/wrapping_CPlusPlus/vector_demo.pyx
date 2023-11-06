# distutils: language = c++

from libcpp.vector cimport vector

cdef vector[int] vect
cdef int i, x

for i in range(10):
    vect.push_back(i)

for i in range(10):
    print(vect[i])

for x in vect:
    print(x)
