# coding: ASCII

# ok:
cdef char* c1   =  "abc"
cdef bytes b1   =  "abc"
cdef str s1     =  "abc"

cdef unicode u1 = u"abc"

cdef bytes b2 = b"abc"
cdef char* c2 = b"abc"

cdef bytes b3 = c1
cdef char* c3 = b1

cdef object o1  =  "abc"
cdef object o2  = b"abc"
cdef object o3  = u"abc"

o4 = c1
o5 = b1
o6 = s1
o7 = u1

# errors:
cdef char* c_f1   = u"abc"
cdef char* c_f2   = u1
cdef char* c_f3   = s1

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


_ERRORS = u"""
26:20: Unicode objects do not support coercion to C types.
27:22: Unicode objects do not support coercion to C types.
28:22: 'str' objects do not support coercion to C types.

30:20: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
31:22: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
32:22: Cannot convert 'str' to 'bytes' implicitly. This is not portable.

34:17: Cannot assign type 'char *' to 'str object'
35:19: Cannot convert 'bytes' object to str implicitly. This is not portable to Py3.
36:17: Cannot convert Unicode string to 'str' implicitly. This is not portable and requires explicit encoding.
37:19: Cannot convert Unicode string to 'str' implicitly. This is not portable and requires explicit encoding.

39:20: str objects do not support coercion to unicode, use a unicode string literal instead (u'')
40:22: str objects do not support coercion to unicode, use a unicode string literal instead (u'')
41:20: Cannot assign type 'char *' to 'unicode object'
42:22: Cannot convert 'bytes' object to unicode implicitly, decoding required
43:22: Cannot convert 'char*' to unicode implicitly, decoding required
"""
