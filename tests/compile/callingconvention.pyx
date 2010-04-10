cdef extern from "callingconvention.h":
    pass


cdef extern int f1()

cdef extern int __cdecl f2()

cdef extern int __stdcall f3()

cdef extern int __fastcall f4()


cdef extern int (*p1)()

cdef extern int (__cdecl *p2)()

cdef extern int (__stdcall *p3)()

cdef extern int (__fastcall *p4)()


p1 = f1
p2 = f2
p3 = f3
p4 = f4
