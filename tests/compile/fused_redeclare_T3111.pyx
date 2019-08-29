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


_WARNINGS = ""
