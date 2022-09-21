# --

ctypedef            int Int0
ctypedef public     int Int1
ctypedef        api int Int2
ctypedef public api int Int3

ctypedef            enum EnumA0: EA0
ctypedef public     enum EnumA1: EA1
ctypedef        api enum EnumA2: EA2
ctypedef public api enum EnumA3: EA3

cdef            enum EnumB0: EB0=0
cdef public     enum EnumB1: EB1=1
cdef        api enum EnumB2: EB2=2
cdef public api enum EnumB3: EB3=3

# --

ctypedef            struct StructA0: 
    int SA0
ctypedef public     struct StructA1: 
    int SA1
ctypedef        api struct StructA2:
    int SA2
ctypedef public api struct StructA3:
    int SA3

cdef            struct StructB0:
    int SB0
cdef public     struct StructB1:
    int SB1
cdef        api struct StructB2:
    int SB2
cdef public api struct StructB3:
    int SB3

# --

ctypedef            class Foo0: pass
ctypedef public     class Foo1 [type PyFoo1_Type, object PyFoo1_Object]: pass
ctypedef        api class Foo2 [type PyFoo2_Type, object PyFoo2_Object]: pass
ctypedef public api class Foo3 [type PyFoo3_Type, object PyFoo3_Object]: pass

cdef            class Bar0: pass
cdef public     class Bar1 [type PyBar1_Type, object PyBar1_Object]: pass
cdef        api class Bar2 [type PyBar2_Type, object PyBar2_Object]: pass
cdef public api class Bar3 [type PyBar3_Type, object PyBar3_Object]: pass

# --

cdef extern from *:
    void foo()

cdef inline     void bar (): pass
cdef            void bar0()
cdef public     void bar1()
cdef        api void bar2()
cdef public api void bar3()

cdef inline     void* spam (object o) except NULL: return NULL
cdef            void* spam0(object o) except NULL
cdef public     void* spam1(object o) except NULL
cdef        api void* spam2(object o) except NULL nogil
cdef public api void* spam3(object o) except NULL with gil

# --

cdef            int i0 = 0 # XXX implement initialization!!!
cdef public     int i1
cdef        api int i2
cdef public api int i3

# --
