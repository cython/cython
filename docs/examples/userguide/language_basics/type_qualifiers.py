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
