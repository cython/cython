# mode: compile
# --

ctypedef            i32 Int0
ctypedef public     i32 Int1
ctypedef        api i32 Int2
ctypedef public api i32 Int3

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
    i32 SA0
ctypedef public     struct StructA1: 
    i32 SA1
ctypedef        api struct StructA2:
    i32 SA2
ctypedef public api struct StructA3:
    i32 SA3

cdef            struct StructB0:
    i32 SB0
cdef public     struct StructB1:
    i32 SB1
cdef        api struct StructB2:
    i32 SB2
cdef public api struct StructB3:
    i32 SB3

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

cdef            void bar0(): pass
cdef public     void bar1(): pass
cdef        api void bar2(): pass
cdef public api void bar3(): pass

cdef            void* spam0(object o) except NULL: return NULL
cdef public     void* spam1(object o) except NULL: return NULL
cdef        api void* spam2(object o) except NULL: return NULL
cdef public api void* spam3(object o) except NULL: return NULL

bar0()
spam0(None)

# --

cdef            f64 d0 = 0
cdef public     f64 d1 = 1
cdef        api f64 d2 = 2
cdef public api f64 d3 = 3

cdef            object o0 = None
cdef public     object o1 = None
cdef        api object o2 = None
cdef public api object o3 = None

# --
