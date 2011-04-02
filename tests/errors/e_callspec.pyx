# mode: error

cimport cython

@cython.callspec("")
cdef void h1(): pass

@cython.callspec("__cdecl")
cdef void __cdecl h2(): pass

@cython.callspec("__stdcall")
cdef void __stdcall h3(): pass

@cython.callspec("__fastcall")
cdef void __fastcall h4(): pass

@cython.callspec("__cdecl")
cdef void __stdcall h5(): pass # fail

@cython.callspec("__cdecl")
cdef void __fastcall h6(): pass # fail

cdef void (*p1)()
cdef void (__cdecl *p2)()
cdef void (__stdcall *p3)()
cdef void (__fastcall *p4)()

p1 = h1
p2 = h2
p3 = h3
p4 = h4

#p1 = h2 # fail
#p1 = h3 # fail
#p1 = h4 # fail

#p2 = h1 # fail
#p2 = h3 # fail
#p2 = h4 # fail

_ERRORS = u"""
18:22: cannot have both '__stdcall' and '__cdecl' calling conventions
21:23: cannot have both '__fastcall' and '__cdecl' calling conventions
"""
#31:14: Cannot assign type 'void (__cdecl )(void)' to 'void (*)(void)'
#32:14: Cannot assign type 'void (__stdcall )(void)' to 'void (*)(void)'
#33:14: Cannot assign type 'void (__fastcall )(void)' to 'void (*)(void)'
#35:14: Cannot assign type 'void (void)' to 'void (__cdecl *)(void)'
#36:14: Cannot assign type 'void (__stdcall )(void)' to 'void (__cdecl *)(void)'
#37:14: Cannot assign type 'void (__fastcall )(void)' to 'void (__cdecl *)(void)'
