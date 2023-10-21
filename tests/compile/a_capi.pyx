# mode: compile

cdef pub struct Foo:
    i32 a, b

ctypedef struct Blarg:
    i32 c, d

ctypedef pub Foo Zax

cdef pub class C[type C_Type, object C_Obj]:
    pass

cdef pub Zax *blarg

cdef pub C c_pub = C()
cdef api C c_api = C()

cdef pub dict o_pub = C()
cdef api list o_api = C()

cdef api f32 f(Foo *x):
    pass

cdef pub void g(Blarg *x):
    pass

cdef pub api void h(Zax *x):
    pass

cdef extern from "a_capi.h":
    pass
