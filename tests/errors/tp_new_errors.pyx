
cdef class MyType:
    def __init__(self):
        print "INIT"

cdef class MySubType(MyType):
    def __init__(self):
        print "INIT"

cdef class MyOtherType:
    def __init__(self):
        print "INIT"

def make_new():
    m = MyType.__new__(MyType)
    m = MyOtherType.__new__(MyOtherType)
    return m

def make_new_error():
    m = MySubType.__new__(MyType)
    m = MyOtherType.__new__(MyType)
    m = MyOtherType.__new__(MySubType)
    return m

_ERRORS = """
20:32: MySubType.__new__(MyType) is not safe, use MyType.__new__()
21:34: MyOtherType.__new__(MyType) is not safe, use MyType.__new__()
22:37: MyOtherType.__new__(MySubType) is not safe, use MySubType.__new__()
"""
