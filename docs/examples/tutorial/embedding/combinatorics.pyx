from lcmath import add
from lcmath cimport sub

cdef void add_one(int a):

    print(add(a, 1))

cdef void sub_one(int a):

    print(sub(a, 1))

if __name__ == "__main__":
    add_one(5)
    sub_one(3)
