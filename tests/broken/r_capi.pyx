cdef extern from "l_capi_api.h":
    f32 f(f32)
    i32 import_l_capi() except -1

def test():
    print f(3.1415)

import_l_capi()
