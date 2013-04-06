# mode: error

cimport cython

ctypedef int USERTYPE

# Functions

@cython.callspec("")
cdef void h1(): pass

@cython.callspec("__cdecl")
cdef void __cdecl h2(): pass

@cython.callspec("__stdcall")
cdef void __stdcall h3(): pass

@cython.callspec("__fastcall")
cdef void __fastcall h4(): pass

cdef USERTYPE h5(): return 0

cdef USERTYPE __cdecl h6(): return 0

cdef USERTYPE __stdcall h7(): return 0

cdef USERTYPE __fastcall h8(): return 0

@cython.callspec("__cdecl")
cdef void __stdcall herr1(): pass # fail

@cython.callspec("__cdecl")
cdef void __fastcall herr2(): pass # fail

# Pointer typedefs

ctypedef void (*PT1)()
ctypedef void (__cdecl *PT2)()
ctypedef void (__stdcall *PT3)()
ctypedef void (__fastcall *PT4)()
ctypedef USERTYPE (*PT5)()
ctypedef USERTYPE (__cdecl *PT6)()
ctypedef USERTYPE (__stdcall *PT7)()
ctypedef USERTYPE (__fastcall *PT8)()

# Pointers

cdef void (*p1)()
cdef void (__cdecl *p2)()
cdef void (__stdcall *p3)()
cdef void (__fastcall *p4)()
cdef USERTYPE (*p5)()
cdef USERTYPE (__cdecl *p6)()
cdef USERTYPE (__stdcall *p7)()
cdef USERTYPE (__fastcall *p8)()

cdef PT1 pt1
cdef PT2 pt2
cdef PT3 pt3
cdef PT4 pt4
cdef PT5 pt5
cdef PT6 pt6
cdef PT7 pt7
cdef PT8 pt8

# Assignments

p1 = pt1 = p2 = pt2 = h1
p1 = pt1 = p2 = pt2 = h2
p3 = pt3 = h3
p4 = pt4 = h4

p5 = pt5 = p6 = pt6 = h5
p5 = pt5 = p6 = pt6 = h6
p7 = pt7 = h7
p8 = pt8 = h8

#p1 = h2 # fail
#p1 = h3 # fail
#p1 = h4 # fail

#p2 = h1 # fail
#p2 = h3 # fail
#p2 = h4 # fail

_ERRORS = u"""
30:25: cannot have both '__stdcall' and '__cdecl' calling conventions
33:26: cannot have both '__fastcall' and '__cdecl' calling conventions
"""
#31:14: Cannot assign type 'void (__cdecl )(void)' to 'void (*)(void)'
#32:14: Cannot assign type 'void (__stdcall )(void)' to 'void (*)(void)'
#33:14: Cannot assign type 'void (__fastcall )(void)' to 'void (*)(void)'
#35:14: Cannot assign type 'void (void)' to 'void (__cdecl *)(void)'
#36:14: Cannot assign type 'void (__stdcall )(void)' to 'void (__cdecl *)(void)'
#37:14: Cannot assign type 'void (__fastcall )(void)' to 'void (__cdecl *)(void)'
