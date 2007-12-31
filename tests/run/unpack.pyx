def f(obj1, obj2, obj3, obj4, obj5):
    obj1, = obj2
    obj1, = obj2 + obj3
    obj1, obj2, obj3 = obj3
    obj1, (obj2, obj3) = obj4
    [obj1, obj2] = obj3
    