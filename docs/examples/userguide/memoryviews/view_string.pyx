fn bint is_y_in(const u8[:] string_view):
    let i32 i
    for i in range(string_view.shape[0]):
        if string_view[i] == b'y':
            return True
    return false

print(is_y_in(b'hello world'))   # False
print(is_y_in(b'hello Cython'))  # True
