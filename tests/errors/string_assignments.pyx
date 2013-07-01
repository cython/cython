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

cdef object o1  =  "abc"
cdef object o2  = b"abc"
cdef object o3  = u"abc"

o4 = c1
o5 = b1
o6 = s1
o7 = u1
o8 = cu1

# errors:
cdef char* c_f1   = u"abc"
cdef char* c_f2   = u1
cdef char* c_f3   = s1

cdef Py_UNICODE* cu_f1 = c1
cdef Py_UNICODE* cu_f2 = b1
cdef Py_UNICODE* cu_f3 = s1
cdef Py_UNICODE* cu_f4 = b"abc"

cdef bytes b_f1   = u"abc"
cdef bytes b_f2   = u1
cdef bytes b_f3   = s1

cdef str s_f1  = b"abc"
cdef str s_f2  = b1
cdef str s_f3  = u"abc"
cdef str s_f4  = u1

cdef unicode u_f1 = "abc"
cdef unicode u_f2 = s1
cdef unicode u_f3 = b"abc"
cdef unicode u_f4 = b1
cdef unicode u_f5 = c1

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

_ERRORS = u"""
29:20: Unicode literals do not support coercion to C types other than Py_UNICODE/Py_UCS4 (for characters) or Py_UNICODE* (for strings).
30:22: Unicode objects only support coercion to Py_UNICODE*.
31:22: 'str' objects do not support coercion to C types (use 'bytes'?).

33:27: Cannot assign type 'char *' to 'Py_UNICODE *'
34:27: Cannot convert 'bytes' object to Py_UNICODE*, use 'unicode'.
35:27: 'str' objects do not support coercion to C types (use 'unicode'?).
36:25: Cannot convert 'bytes' object to Py_UNICODE*, use 'unicode'.

38:20: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
39:22: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
40:22: Cannot convert 'str' to 'bytes' implicitly. This is not portable.

42:17: Cannot convert 'bytes' object to str implicitly. This is not portable to Py3.
43:19: Cannot convert 'bytes' object to str implicitly. This is not portable to Py3.
44:17: Cannot convert Unicode string to 'str' implicitly. This is not portable and requires explicit encoding.
45:19: Cannot convert Unicode string to 'str' implicitly. This is not portable and requires explicit encoding.

47:20: str objects do not support coercion to unicode, use a unicode string literal instead (u'')
48:22: str objects do not support coercion to unicode, use a unicode string literal instead (u'')
49:20: Cannot convert 'bytes' object to unicode implicitly, decoding required
50:22: Cannot convert 'bytes' object to unicode implicitly, decoding required
51:22: Cannot convert 'char*' to unicode implicitly, decoding required

53:19: Cannot assign type 'str object' to 'tuple object'
54:18: Cannot assign type 'unicode object' to 'tuple object'
55:18: Cannot assign type 'bytes object' to 'tuple object'

61:13: default encoding required for conversion from 'char *' to 'str object'
62:13: default encoding required for conversion from 'char *' to 'str object'
63:17: Cannot convert 'char*' to unicode implicitly, decoding required
64:17: default encoding required for conversion from 'char *' to 'unicode object'
"""
