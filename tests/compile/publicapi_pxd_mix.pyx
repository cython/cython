# mode: compile

cdef class Foo1: pass
cdef class Foo2: pass
cdef class Foo3: pass

cdef class Bar1: pass
cdef class Bar2: pass
cdef class Bar3: pass

cdef         void bar0(): pass
cdef pub     void bar1(): pass
cdef     api void bar2(): pass
cdef pub api void bar3(): pass

cdef         void* spam0(object o) except NULL: return NULL
cdef pub     void* spam1(object o) except NULL: return NULL
cdef     api void* spam2(object o) except NULL nogil: return NULL
cdef pub api void* spam3(object o) except NULL with gil: return NULL

cdef         i32 i0 = 0 # XXX This should not be required!
cdef pub     i32 i1 = 1
cdef     api i32 i2 = 2
cdef pub api i32 i3 = 3
