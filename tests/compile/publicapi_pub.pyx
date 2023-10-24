# mode: compile
# --

ctypedef     i32 Int0
ctypedef pub i32 Int1

ctypedef     enum EnumA0: EA0
ctypedef pub enum EnumA1: EA1

cdef enum EnumB0: EB0=0
pub  enum EnumB1: EB1=1

cdef Int0   i0  = 0
cdef EnumA0 ea0 = EA0
cdef EnumB0 eb0 = EB0

pub Int1   i1  = 0
pub EnumA1 ea1 = EA1
pub EnumB1 eb1 = EB1

# --

ctypedef     struct StructA0:
    i32 SA0
ctypedef pub struct StructA1:
    i32 SA1

struct StructB0:
    i32 SB0
pub struct StructB1:
    i32 SB1

cdef StructA0 sa0 = {'SA0':0}
cdef StructB0 sb0 = {'SB0':2}

pub StructA1 sa1 = {'SA1':1}
pub StructB1 sb1 = {'SB1':3}

# --

ctypedef     class Foo0: pass
ctypedef pub class Foo1 [type PyFoo1_Type, object PyFoo1_Object]: pass

cdef class Bar0: pass
pub  class Bar1 [type PyBar1_Type, object PyBar1_Object]: pass

cdef Foo0 f0 = None
cdef Bar0 b0 = None

pub Foo1 f1 = None
pub Bar1 b1 = None

# --

cdef void bar0(): pass
pub  void bar1(): pass

cdef void* spam0(object o) except NULL: return NULL
pub  void* spam1(object o) except NULL: return NULL

bar0()
bar1()
spam0(None)
spam1(None)

# --
