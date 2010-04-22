cdef extern from "declarations.h":
    pass

cdef extern char *cp
cdef extern char *cpa[5]
cdef extern int (*ifnpa[5])()
cdef extern char *(*cpfnpa[5])()
cdef extern int (*ifnp)()
cdef extern int (*iap)[5]

cdef extern int ifn()
cdef extern char *cpfn()
cdef extern int (*iapfn())[5]
cdef extern char *(*cpapfn())[5]
cdef extern int fnargfn(int ())

cdef extern int ia[]
cdef extern int iaa[][3]
cdef extern int a(int[][3], int[][3][5])

cdef void f():
    cdef void *p=NULL
    global ifnp, cpa
    ifnp = <int (*)()>p

cdef char *g():
    pass

f()
g()
