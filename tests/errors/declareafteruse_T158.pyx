# ticket: t158
# mode: error

def mult_decl_test():
    print "%s" % vv
    print "%s" % s
    cdef str s, vv = "Test"

def def_test():
    cdef int j = 10
    i[0] = j
    cdef int *i = NULL # pointer variables are special case

cdef cdef_test():
    cdef int j = 10
    i[0] = j
    print "%d" % i[0]
    cdef int *i = NULL

cpdef cpdef_test():
    cdef int j = 10
    i[0] = j
    print "%d" % i[0]
    cdef int *i = NULL

s.upper()
cdef str s = "Test"

class Foo(object):
    def bar(self, x, y):
        cdef unsigned long w = 20
        z = w + t
        cdef int t = 10

cdef class Foo2(object):
    print '%s' % r # check error inside class scope
    cdef str r
    def bar(self, x, y):
        cdef unsigned long w = 20
        self.r = c'r'
        print self.r
        z = w + g(t)
        cdef int t = 10

def g(x):
    return x

cdef int d = 20
baz[0] = d
cdef int *baz

print var[0][0]
cdef unsigned long long[100][100] var

_ERRORS = u"""
5:17: local variable 'vv' referenced before assignment
6:17: local variable 's' referenced before assignment
7:13: cdef variable 's' declared after it is used
7:16: cdef variable 'vv' declared after it is used
12:14: cdef variable 'i' declared after it is used
18:14: cdef variable 'i' declared after it is used
24:14: cdef variable 'i' declared after it is used
27:9: cdef variable 's' declared after it is used
33:17: cdef variable 't' declared after it is used
43:17: cdef variable 't' declared after it is used
50:10: cdef variable 'baz' declared after it is used
53:34: cdef variable 'var' declared after it is used
"""
# FIXME not detected
#37:13: cdef variable 'r' declared after it is used
