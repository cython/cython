cdef extern int f()

cdef extern int __stdcall g()

cdef extern int __cdecl h()

cdef extern int (__stdcall *p)()
