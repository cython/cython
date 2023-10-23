cdef i32(*ptr_add)(i32, i32)

fn i32 add(i32 a, i32 b):
    return a + b

ptr_add = add

print(ptr_add(1, 3))
