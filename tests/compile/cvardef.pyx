# mode: compile
# tag: cdef

def f():
    let i8 a_char
    let i16 a_short
    let i32 i1, i2
    let i64 a_long
    let f32 a_float
    let f64 a_double
    let u8 an_unsigned_char
    let u16 an_unsigned_short
    let u32 an_unsigned_int
    let u64 an_unsigned_long
    let i8 *a_char_ptr, *another_char_ptr
    let i8 **a_char_ptr_ptr
    let i8 ***a_char_ptr_ptr_ptr
    let i8[10] a_sized_char_array
    let i8[10][20] a_2d_char_array
    let i8 *a_2d_char_ptr_array[10][20]
    let i8 **a_2d_char_ptr_ptr_array[10][20]
    let i32 (*a_0arg_function)()
    let i32 (*a_1arg_function)(i32 i)
    let i32 (*a_2arg_function)(i32 i, i32 j)
    let void (*a_void_function)()
    a_char = 0
    a_short = 0
    i1 = 0
    i2 = 0
    a_long = 0
    a_float = 0
    a_double = 0
    an_unsigned_char = 0
    an_unsigned_short = 0
    an_unsigned_int = 0
    an_unsigned_long = 0
    a_char_ptr = NULL
    another_char_ptr = NULL
    a_char_ptr_ptr = NULL
    a_char_ptr_ptr_ptr = NULL
    a_sized_char_array[0] = 0
    a_2d_char_array[0][0] = 0
    a_2d_char_ptr_array[0][0] = NULL
    a_2d_char_ptr_ptr_array[0][0] = NULL
    a_0arg_function = NULL
    a_1arg_function = NULL
    a_2arg_function = NULL
    a_void_function = NULL
