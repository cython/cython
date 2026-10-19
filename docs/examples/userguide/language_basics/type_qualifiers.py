def use_volatile():
    i: cython.volatile[cython.int] = 5

@cython.cfunc
def sum(a: cython.const[cython.int], b: cython.const[cython.int]) -> cython.const[cython.int]:
    return a + b

@cython.cfunc
def pointer_to_const_int(value: cython.pointer[cython.const[cython.int]]) -> cython.void:
    # Declares value as pointer to const int type (alias: "cython.p_const_int").
    # The value can be modified but the object pointed to by value cannot be modified.
    new_value: cython.int = 10
    print(value[0])
    value = cython.address(new_value)
    print(value[0])

@cython.cfunc
def const_pointer_to_int(value: cython.const[cython.pointer[cython.int]]) -> cython.void:
    # Declares value as const pointer to int type (alias: "cython.const[cython.p_int]").
    # Value cannot be modified but the object pointed to by value can be modified.
    print(value[0])
    value[0] = 10
    print(value[0])

@cython.cfunc
def const_pointer_to_const_int(value: cython.const[cython.pointer[cython.const[cython.int]]]) -> cython.void:
    # Declares value as const pointer to const int type (alias: "cython.const[cython.p_const_int]").
    # Neither the value variable nor the int pointed to can be modified.
    print(value[0])

@cython.cfunc
def vector_add(
    a: cython.restrict[cython.pointer[cython.const[cython.int]]],
    b: cython.restrict[cython.pointer[cython.const[cython.int]]],
    result: cython.restrict[cython.pointer[cython.int]],
    n: cython.int
) -> cython.void:
    # Declares a, b and result as restrict pointers. Restrict pointers are a promise to the compiler
    # that for the lifetime of the pointer, only it or a value directly derived from it (such as a + 1)
    # will be used to access the object to which it points. This allows for certain optimizations such as loop vectorization.
    for i in range(n):
        result[i] = a[i] + b[i]
