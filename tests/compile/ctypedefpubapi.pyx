# mode: compile

ctypedef public api class Foo [type PyFoo_Type, object PyFooObject]:
    pass

cdef api:
    ctypedef public class Bar [type PyBar_Type, object PyBarObject]:
        pass

cdef public api:
    ctypedef class Baz [type PyBaz_Type, object PyBazObject]:
        pass
