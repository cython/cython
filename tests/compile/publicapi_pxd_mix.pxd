# --

ctypedef         i32 Int0
ctypedef pub     i32 Int1
ctypedef     api i32 Int2
ctypedef pub api i32 Int3

ctypedef         enum EnumA0: EA0
ctypedef pub     enum EnumA1: EA1
ctypedef     api enum EnumA2: EA2
ctypedef pub api enum EnumA3: EA3

cdef     enum EnumB0: EB0=0
pub      enum EnumB1: EB1=1
cdef api enum EnumB2: EB2=2
pub  api enum EnumB3: EB3=3

# --

ctypedef         struct StructA0: 
    i32 SA0
ctypedef pub     struct StructA1: 
    i32 SA1
ctypedef     api struct StructA2:
    i32 SA2
ctypedef pub api struct StructA3:
    i32 SA3

struct StructB0:
    i32 SB0
pub struct StructB1:
    i32 SB1
cdef api struct StructB2:
    i32 SB2
pub  api struct StructB3:
    i32 SB3

# --

ctypedef         class Foo0: pass
ctypedef pub     class Foo1 [type PyFoo1_Type, object PyFoo1_Object]: pass
ctypedef     api class Foo2 [type PyFoo2_Type, object PyFoo2_Object]: pass
ctypedef pub api class Foo3 [type PyFoo3_Type, object PyFoo3_Object]: pass

cdef     class Bar0: pass
pub      class Bar1 [type PyBar1_Type, object PyBar1_Object]: pass
cdef api class Bar2 [type PyBar2_Type, object PyBar2_Object]: pass
pub  api class Bar3 [type PyBar3_Type, object PyBar3_Object]: pass

# --

extern from *:
    void foo()

fn inline       void bar (): pass
fn              void bar0()
pub             void bar1()
cdef        api void bar2()
pub         api void bar3()

fn inline       void* spam (object o) except NULL: return NULL
fn              void* spam0(object o) except NULL
pub             void* spam1(object o) except NULL
cdef        api void* spam2(object o) except NULL nogil
pub         api void* spam3(object o) except NULL with gil

# --

cdef     i32 i0 = 0 # XXX implement initialization!!!
pub      i32 i1
cdef api i32 i2
pub  api i32 i3

# --
