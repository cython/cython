# mode: compile

cdef class Foo1: pass
cdef class Foo2: pass
cdef class Foo3: pass

cdef class Bar1: pass
cdef class Bar2: pass
cdef class Bar3: pass

cdef            void bar0(): pass
cdef public     void bar1(): pass
cdef        api void bar2(): pass
cdef public api void bar3(): pass

cdef            void* spam0(object o) except NULL: return NULL
cdef public     void* spam1(object o) except NULL: return NULL
cdef        api void* spam2(object o) nogil except NULL: return NULL
cdef public api void* spam3(object o) except NULL with gil: return NULL
