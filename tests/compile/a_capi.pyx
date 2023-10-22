# mode: compile

pub struct Foo:
    i32 a, b

ctypedef struct Blarg:
    i32 c, d

ctypedef pub Foo Zax

pub class C[type C_Type, object C_Obj]:
    pass

pub Zax *blarg

pub C c_pub = C()
cdef api C c_api = C()

pub dict o_pub = C()
cdef api list o_api = C()

cdef api f32 f(Foo *x):
    pass

pub void g(Blarg *x):
    pass

pub api void h(Zax *x):
    pass

cdef extern from "a_capi.h":
    pass
