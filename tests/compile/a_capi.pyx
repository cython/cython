# mode: compile

cdef public struct Foo:
    i32 a, b

ctypedef struct Blarg:
    i32 c, d

ctypedef public Foo Zax

cdef public class C[type C_Type, object C_Obj]:
    pass

cdef public Zax *blarg

cdef public C c_pub = C()
cdef api    C c_api = C()

cdef public dict o_pub = C()
cdef api    list o_api = C()

cdef api f32 f(Foo *x):
    pass

cdef public void g(Blarg *x):
    pass

cdef public api void h(Zax *x):
    pass

cdef extern from "a_capi.h":
    pass
