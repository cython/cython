# mode: error

fn i32 exceptmaybeminus2(i32 bad) except ?-2:
    if bad:
        raise RuntimeError
    else:
        return 0

def fail_exceptmaybeminus2(bad):
    let i32 (*fptr_a)(i32) except -2
    let i32 (*fptr_b)(i32) except -1
    let i32 (*fptr_c)(i32) except ?-1
    fptr_a = exceptmaybeminus2
    fptr_b = exceptmaybeminus2
    fptr_c = exceptmaybeminus2

extern from *:
    # define this as extern since Cython converts internal "except*" to "except -1"
    fn i32 exceptstar(i32 bad) except *

    struct mystruct:
        i32 (*func_ptr)(i32 param) nogil
        void (*func_ptr_void)(i32 param) nogil

def fail_exceptstar(bad):
    let i32 (*fptr_a)(i32) noexcept
    let i32 (*fptr_b)(i32) except -1
    let i32 (*fptr_c)(i32) except ?-1
    fptr_a = exceptstar
    fptr_b = exceptstar
    fptr_c = exceptstar

fn i32 cb(i32 param) nogil:
    return param

fn void cb_void(i32 param) except * nogil:
    return

def fail_struct_pointer():
    let mystruct ms = mystruct(&cb, &cb_void)


_ERRORS = """
13:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except -2'. Exception values are incompatible.
14:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except -1'. Exception values are incompatible.
15:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except? -1'. Exception values are incompatible.
29:13: Cannot assign type 'int (int) except *' to 'int (*)(int) noexcept'. Exception values are incompatible. Suggest adding 'noexcept' to type 'int (int) except *'.
30:13: Cannot assign type 'int (int) except *' to 'int (*)(int) except -1'. Exception values are incompatible.
31:13: Cannot assign type 'int (int) except *' to 'int (*)(int) except? -1'. Exception values are incompatible.
40:31: Cannot assign type 'int (*)(int) except? -1 nogil' to 'int (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to type 'int (int) except? -1 nogil'.
40:31: Cannot assign type 'int (*)(int) except? -1 nogil' to 'int (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to type 'int (int) except? -1 nogil'.
40:36: Cannot assign type 'void (*)(int) except * nogil' to 'void (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to type 'void (int) except * nogil'.
40:36: Cannot assign type 'void (*)(int) except * nogil' to 'void (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to type 'void (int) except * nogil'.
"""
