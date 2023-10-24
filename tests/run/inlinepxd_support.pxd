
fn inline i32 my_add(i32 a, i32 b=1, i32 c=0):
    return a + b + c

fn inline index(list L):
    # This function should *not* be affected by directives set in the outer scope, such as "wraparound".
    # See https://github.com/cython/cython/issues/1071
    return L[-1]

fn inline call_index(list L):
    return index(L)
