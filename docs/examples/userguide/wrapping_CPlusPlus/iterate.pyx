# distutils: language = c++

from libcpp.vector cimport vector

def main():
    cdef vector[int] v = [4, 6, 5, 10, 3]

    cdef int value
    for value in v:
        print(value)

    return [x*x for x in v if x % 2 == 0]
