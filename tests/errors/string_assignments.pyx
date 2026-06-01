# mode: error
# coding: ASCII
# tag: py_unicode_strings

# ok:
cdef char* c1   =  "abc"
cdef str s1     =  "abc"

cdef unicode u1 = u"abc"
cdef Py_UNICODE* cu1 = u1

cdef bytes b1 = b"abc"
cdef char* c2 = b"abc"

cdef bytes b2 = c1
cdef char* c3 = b1

cdef basestring bs1  =  "abc"
cdef basestring bs2  = u"abc"

cdef object o1  =  "abc"
cdef object o2  = b"abc"
cdef object o3  = u"abc"

o4 = c1
o5 = b1
o6 = s1
o7 = u1
o8 = cu1
o9 = bs1

u1 = bs1
s1 = bs1

# errors:
cdef char* c_f1   = u"\N{SNOWMAN}"  # not bytes compatible
cdef char* c_f2   = u1
cdef char* c_f3   = s1

cdef Py_UNICODE* cu_f1 = c1
cdef Py_UNICODE* cu_f2 = b1
cdef Py_UNICODE* cu_f3 = s1
cdef Py_UNICODE* cu_f4 = b"abc"

cdef bytes b_f1   = u"abc"
cdef bytes b_f2   = u1
cdef bytes b_f3   = s1
cdef bytes b_f4   = bs1

cdef str s_f1  = b"abc"
cdef str s_f2  = b1
cdef str s_f3  = u"abc"
cdef str s_f4  = u1

cdef unicode u_f1 = "abc"
cdef unicode u_f2 = s1
cdef unicode u_f3 = b"abc"
cdef unicode u_f4 = b1
cdef unicode u_f5 = c1

cdef basestring bs_f1 = b"abc"
cdef basestring bs_f2 = b1

cdef tuple t_f1 =  "abc"
cdef tuple t_f2 = u"abc"
cdef tuple t_f3 = b"abc"

cdef list  l_f1 = s1
cdef list  l_f2 = b1
cdef list  l_f3 = u1

print <str>c1
print <str>c1[1:2]
print <unicode>c1
print <unicode>c1[1:2]

cdef void* v_f1   = u"\N{SNOWMAN}"  # not bytes compatible


# ok again:

cdef void* v1 =  "abc"
cdef void* v2 = b"abc"
cdef void* v3 = u"abc"

cdef voidptr_func(void* x): pass

voidptr_func( "abc")
voidptr_func(b"abc")
voidptr_func(u"abc")


_ERRORS = u"""
36:20: Unicode literals do not support coercion to C types other than Py_UCS4/Py_UNICODE (for characters), Py_UNICODE* (for strings) or char*/void* (for auto-encoded strings).
37:20: Unicode objects only support coercion to Py_UNICODE*.
38:20: Unicode objects only support coercion to Py_UNICODE*.

40:25: Cannot assign type 'char *' to 'Py_UNICODE *'
41:25: Cannot convert 'bytes' object to Py_UNICODE*, use 'str'.
43:25: Cannot convert 'bytes' object to Py_UNICODE*, use 'str'.

45:20: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
46:20: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
47:20: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
48:20: Cannot convert Unicode string to 'bytes' implicitly, encoding required.

50:17: Cannot convert 'bytes' object to str implicitly, decoding required
51:17: Cannot convert 'bytes' object to str implicitly, decoding required

57:20: Cannot convert 'bytes' object to str implicitly, decoding required
58:20: Cannot convert 'bytes' object to str implicitly, decoding required
59:20: Cannot convert 'char*' to unicode implicitly, decoding required

61:24: Cannot convert 'bytes' object to str implicitly, decoding required
62:24: Cannot convert 'bytes' object to str implicitly, decoding required

64:19: Cannot assign type 'str object' to 'tuple object'
65:18: Cannot assign type 'str object' to 'tuple object'
66:18: Cannot assign type 'bytes object' to 'tuple object'

72:11: Cannot convert 'char*' to unicode implicitly, decoding required
73:13: default encoding required for conversion from 'char *' to 'str object'
74:15: Cannot convert 'char*' to unicode implicitly, decoding required
75:17: default encoding required for conversion from 'char *' to 'str object'
77:20: Unicode literals do not support coercion to C types other than Py_UCS4/Py_UNICODE (for characters), Py_UNICODE* (for strings) or char*/void* (for auto-encoded strings).
"""
