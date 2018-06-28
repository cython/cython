# distutils: language = c++

from libcpp.vector cimport vector

def main():
    cdef vector[int] v
    cdef int i, value

    for i in range(10):
        v.push_back(i)

    for value in v:
        print(value)

    return [x*x for x in v if x % 2 == 0]
