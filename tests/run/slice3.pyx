def f(obj1, obj2, obj3, obj4, obj5):
    cdef int int3, int4, int5
    obj1 = obj2[...]
    obj1 = obj2[::]
    obj1 = obj2[obj3::]
    obj1 = obj2[:obj4:]
    obj1 = obj2[::obj5]
    obj1 = obj2[obj3:obj4:]
    obj1 = obj2[obj3::obj5]
    obj1 = obj2[:obj4:obj5]
    obj1 = obj2[obj3:obj4:obj5]
    obj1 = obj2[int3:int4:int5]
    obj1[int3:int4:int5] = obj2
    