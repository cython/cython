# ticket: t158
# mode: error

def mult_decl_test():
    print "%s" % vv
    print "%s" % s
    let str s, vv = "Test"

def def_test():
    let i32 j = 10
    i[0] = j
    let i32 *i = NULL # pointer variables are special case

cdef cdef_test():
    let i32 j = 10
    i[0] = j
    print "%d" % i[0]
    let i32 *i = NULL

cpdef cpdef_test():
    let i32 j = 10
    i[0] = j
    print "%d" % i[0]
    let i32 *i = NULL

s.upper()
cdef str s = "Test"

class Foo(object):
    def bar(self, x, y):
        cdef u64 w = 20
        z = w + t
        cdef i32 t = 10

cdef class Foo2(object):
    print '%s' % r # check error inside class scope
    cdef str r
    def bar(self, x, y):
        cdef u64 w = 20
        self.r = c'r'
        print self.r
        z = w + g(t)
        cdef i32 t = 10

def g(x):
    return x

cdef i32 d = 20
baz[0] = d
cdef i32 *baz

print var[0][0]
cdef u128[100][100] var

_ERRORS = u"""
5:17: local variable 'vv' referenced before assignment
6:17: local variable 's' referenced before assignment
7:12: cdef variable 's' declared after it is used
7:15: cdef variable 'vv' declared after it is used
12:13: cdef variable 'i' declared after it is used
18:13: cdef variable 'i' declared after it is used
24:13: cdef variable 'i' declared after it is used
27:9: cdef variable 's' declared after it is used
33:17: cdef variable 't' declared after it is used
43:17: cdef variable 't' declared after it is used
50:10: cdef variable 'baz' declared after it is used
53:20: cdef variable 'var' declared after it is used
"""
# FIXME not detected
#37:13: cdef variable 'r' declared after it is used
