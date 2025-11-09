cpdef tuple func(dict foo, int bar):
    foo["hello world"] = 3 + bar
    return foo, 5