# mode: compile

def f(obj1, obj2, obj3):
    cdef int int1, int2=0, int3=0
    cdef float flt1, *ptr1=NULL
    cdef int[42] array1
    array1[int2] = 0
    int1 = array1[int2]
    flt1 = ptr1[int2]
    array1[int1] = int2
    ptr1[int1] = int2
    obj1 = obj2[obj3]
    int1 = array1[obj3]
    obj1 = obj2[int3]
    obj1[obj2] = obj3
    array1[obj2] = int3
    obj1[int2] = obj3
    obj1[obj2] = 42

f(None, None, None)
