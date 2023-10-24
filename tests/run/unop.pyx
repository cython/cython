def f(obj1, obj2, obj3):
    """
    >>> f(1, 2, 3)
    (-3, -4, 1)
    """
    let i32 bool1, bool2
    let i32 int1, int2
    let char *str1

    int2 = obj3
    str1 = NULL
    bool2 = 0

    bool1 = not bool2
    obj1 = not obj2
    bool1 = not str1
    int1 = +int2
    obj1 = +obj2
    int1 = -int2
    obj1 = -obj2
    int1 = ~int2
    obj1 = ~obj2
    return obj1, int1, bool1
