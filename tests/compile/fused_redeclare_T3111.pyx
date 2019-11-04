# ticket: 3111
# mode: compile
# tag: warnings

ctypedef unsigned char npy_uint8
ctypedef unsigned short npy_uint16


ctypedef fused dtype_t:
    npy_uint8

ctypedef fused dtype_t_out:
    npy_uint8
    npy_uint16


def foo(dtype_t[:] a, dtype_t_out[:, :] b):
    pass


# The primary thing we're trying to test here is the _absence_ of the warning
# "__pyxutil:16:4: '___pyx_npy_uint8' redeclared".  The remaining warnings are
# unrelated to this test.
_WARNINGS = """
22:10: 'cpdef_method' redeclared
33:10: 'cpdef_cname_method' redeclared
446:72: Argument evaluation order in C function call is undefined and may not be as expected
446:72: Argument evaluation order in C function call is undefined and may not be as expected
749:34: Argument evaluation order in C function call is undefined and may not be as expected
749:34: Argument evaluation order in C function call is undefined and may not be as expected
943:27: Ambiguous exception value, same as default return value: 0
943:27: Ambiguous exception value, same as default return value: 0
974:29: Ambiguous exception value, same as default return value: 0
974:29: Ambiguous exception value, same as default return value: 0
1002:46: Ambiguous exception value, same as default return value: 0
1002:46: Ambiguous exception value, same as default return value: 0
1092:29: Ambiguous exception value, same as default return value: 0
1092:29: Ambiguous exception value, same as default return value: 0
"""
