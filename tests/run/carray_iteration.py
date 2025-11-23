# mode: run
# tag: forin, carray, bytes, unicode

# GENERATED TEST CODE
# Run me as a Python script to regenerate my test code.
# If things go wrong, delete all lines between the START/END markers and rerun.
# Tests marked with "@cython.test_fail_if_path_exists()" are not currently optimised (but might be later.)

import cython

if cython.compiled:
    charlist = list
else:
    def charlist(l):
        return [ord(ch) for ch in l]


###### START: generated test code ######
#  620 tests optimised using CArrayNode
#  430 tests not optimised


def test_carray_forin_constant_int_1_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_int_1_constant_arg(4)
    [0, 4]
    """
    carray: cython.int[2] = [0, arg]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_1_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_int_1_constant_arg(4))
    [0, 4]
    """
    carray: cython.int[2] = [0, arg]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_1_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_int_1_constant_arg(4)
    [0, 4]
    """
    carray: cython.int[2] = [0, arg]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_1_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_int_1_constant_arg(4))
    [0, 4]
    """
    carray: cython.int[2] = [0, arg]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_1_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_int_1_constant_arg(4))
    [0, 4]
    """
    carray: cython.int[2] = [0, arg]

    return (item for item in carray)  # cython.int



def test_carray_forin_constant_int_1_constant():
    """
    >>> test_carray_forin_constant_int_1_constant()
    [0]
    """
    carray: cython.int[1] = [0]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_1_constant():
    """
    >>> list(test_carray_generator_constant_int_1_constant())
    [0]
    """
    carray: cython.int[1] = [0]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_1_constant():
    """
    >>> test_carray_listcomp_constant_int_1_constant()
    [0]
    """
    carray: cython.int[1] = [0]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_int_1_constant())
    [0]
    """
    carray: cython.int[1] = [0]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_1_constant():
    """
    >>> list(test_carray_genexpr_constant_int_1_constant())
    [0]
    """
    carray: cython.int[1] = [0]

    return (item for item in carray)  # cython.int



def test_literal_forin_literal_int_1_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_int_1_literal_arg(4)
    [0, 4]
    """


    items = []
    for item in [0, arg]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_1_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_int_1_literal_arg(4))
    [0, 4]
    """


    for item in [0, arg]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_1_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_int_1_literal_arg(4)
    [0, 4]
    """


    return [item for item in [0, arg]]  # cython.int



def test_literal_setcomp_literal_int_1_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_int_1_literal_arg(4))
    [0, 4]
    """


    return {item for item in [0, arg]}  # cython.int



def test_literal_genexpr_literal_int_1_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_int_1_literal_arg(4))
    [0, 4]
    """


    return (item for item in [0, arg])  # cython.int



def test_literal_forin_literal_int_1_literal():
    """
    >>> test_literal_forin_literal_int_1_literal()
    [0]
    """


    items = []
    for item in [0]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_1_literal():
    """
    >>> list(test_literal_generator_literal_int_1_literal())
    [0]
    """


    for item in [0]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_1_literal():
    """
    >>> test_literal_listcomp_literal_int_1_literal()
    [0]
    """


    return [item for item in [0]]  # cython.int



def test_literal_setcomp_literal_int_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_int_1_literal())
    [0]
    """


    return {item for item in [0]}  # cython.int



def test_literal_genexpr_literal_int_1_literal():
    """
    >>> list(test_literal_genexpr_literal_int_1_literal())
    [0]
    """


    return (item for item in [0])  # cython.int



def test_carray_forin_pointer_int_1_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_int_1_pointer_arg(4)
    [0, 4]
    """
    carray: cython.pointer[cython.int] = [0, arg]

    items = []
    for item in carray[:2]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_1_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_int_1_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.int] = [0, arg]

    for item in carray[:2]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_1_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_int_1_pointer_arg(4)
    [0, 4]
    """
    carray: cython.pointer[cython.int] = [0, arg]

    return [item for item in carray[:2]]  # cython.int



def test_carray_setcomp_pointer_int_1_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_int_1_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.int] = [0, arg]

    return {item for item in carray[:2]}  # cython.int



def test_carray_genexpr_pointer_int_1_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_int_1_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.int] = [0, arg]

    return (item for item in carray[:2])  # cython.int



def test_carray_forin_pointer_int_1_pointer():
    """
    >>> test_carray_forin_pointer_int_1_pointer()
    [0]
    """
    carray: cython.pointer[cython.int] = [0]

    items = []
    for item in carray[:1]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_1_pointer():
    """
    >>> list(test_carray_generator_pointer_int_1_pointer())
    [0]
    """
    carray: cython.pointer[cython.int] = [0]

    for item in carray[:1]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_1_pointer():
    """
    >>> test_carray_listcomp_pointer_int_1_pointer()
    [0]
    """
    carray: cython.pointer[cython.int] = [0]

    return [item for item in carray[:1]]  # cython.int



def test_carray_setcomp_pointer_int_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_int_1_pointer())
    [0]
    """
    carray: cython.pointer[cython.int] = [0]

    return {item for item in carray[:1]}  # cython.int



def test_carray_genexpr_pointer_int_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_int_1_pointer())
    [0]
    """
    carray: cython.pointer[cython.int] = [0]

    return (item for item in carray[:1])  # cython.int



def test_carray_forin_constant_int_2_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_int_2_constant_arg(4)
    [0, 0, 4]
    """
    carray: cython.int[3] = [0, 0, arg]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_2_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_int_2_constant_arg(4))
    [0, 0, 4]
    """
    carray: cython.int[3] = [0, 0, arg]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_2_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_int_2_constant_arg(4)
    [0, 0, 4]
    """
    carray: cython.int[3] = [0, 0, arg]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_2_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_int_2_constant_arg(4))
    [0, 4]
    """
    carray: cython.int[3] = [0, 0, arg]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_2_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_int_2_constant_arg(4))
    [0, 0, 4]
    """
    carray: cython.int[3] = [0, 0, arg]

    return (item for item in carray)  # cython.int



def test_carray_forin_constant_int_2_constant():
    """
    >>> test_carray_forin_constant_int_2_constant()
    [0, 0]
    """
    carray: cython.int[2] = [0, 0]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_2_constant():
    """
    >>> list(test_carray_generator_constant_int_2_constant())
    [0, 0]
    """
    carray: cython.int[2] = [0, 0]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_2_constant():
    """
    >>> test_carray_listcomp_constant_int_2_constant()
    [0, 0]
    """
    carray: cython.int[2] = [0, 0]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_2_constant():
    """
    >>> sorted(test_carray_setcomp_constant_int_2_constant())
    [0]
    """
    carray: cython.int[2] = [0, 0]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_2_constant():
    """
    >>> list(test_carray_genexpr_constant_int_2_constant())
    [0, 0]
    """
    carray: cython.int[2] = [0, 0]

    return (item for item in carray)  # cython.int



def test_literal_forin_literal_int_2_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_int_2_literal_arg(4)
    [0, 0, 4]
    """


    items = []
    for item in [0, 0, arg]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_2_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_int_2_literal_arg(4))
    [0, 0, 4]
    """


    for item in [0, 0, arg]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_2_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_int_2_literal_arg(4)
    [0, 0, 4]
    """


    return [item for item in [0, 0, arg]]  # cython.int



def test_literal_setcomp_literal_int_2_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_int_2_literal_arg(4))
    [0, 4]
    """


    return {item for item in [0, 0, arg]}  # cython.int



def test_literal_genexpr_literal_int_2_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_int_2_literal_arg(4))
    [0, 0, 4]
    """


    return (item for item in [0, 0, arg])  # cython.int



def test_literal_forin_literal_int_2_literal():
    """
    >>> test_literal_forin_literal_int_2_literal()
    [0, 0]
    """


    items = []
    for item in [0, 0]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_2_literal():
    """
    >>> list(test_literal_generator_literal_int_2_literal())
    [0, 0]
    """


    for item in [0, 0]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_2_literal():
    """
    >>> test_literal_listcomp_literal_int_2_literal()
    [0, 0]
    """


    return [item for item in [0, 0]]  # cython.int



def test_literal_setcomp_literal_int_2_literal():
    """
    >>> sorted(test_literal_setcomp_literal_int_2_literal())
    [0]
    """


    return {item for item in [0, 0]}  # cython.int



def test_literal_genexpr_literal_int_2_literal():
    """
    >>> list(test_literal_genexpr_literal_int_2_literal())
    [0, 0]
    """


    return (item for item in [0, 0])  # cython.int



def test_carray_forin_pointer_int_2_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_int_2_pointer_arg(4)
    [0, 0, 4]
    """
    carray: cython.pointer[cython.int] = [0, 0, arg]

    items = []
    for item in carray[:3]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_2_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_int_2_pointer_arg(4))
    [0, 0, 4]
    """
    carray: cython.pointer[cython.int] = [0, 0, arg]

    for item in carray[:3]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_2_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_int_2_pointer_arg(4)
    [0, 0, 4]
    """
    carray: cython.pointer[cython.int] = [0, 0, arg]

    return [item for item in carray[:3]]  # cython.int



def test_carray_setcomp_pointer_int_2_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_int_2_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.int] = [0, 0, arg]

    return {item for item in carray[:3]}  # cython.int



def test_carray_genexpr_pointer_int_2_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_int_2_pointer_arg(4))
    [0, 0, 4]
    """
    carray: cython.pointer[cython.int] = [0, 0, arg]

    return (item for item in carray[:3])  # cython.int



def test_carray_forin_pointer_int_2_pointer():
    """
    >>> test_carray_forin_pointer_int_2_pointer()
    [0, 0]
    """
    carray: cython.pointer[cython.int] = [0, 0]

    items = []
    for item in carray[:2]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_2_pointer():
    """
    >>> list(test_carray_generator_pointer_int_2_pointer())
    [0, 0]
    """
    carray: cython.pointer[cython.int] = [0, 0]

    for item in carray[:2]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_2_pointer():
    """
    >>> test_carray_listcomp_pointer_int_2_pointer()
    [0, 0]
    """
    carray: cython.pointer[cython.int] = [0, 0]

    return [item for item in carray[:2]]  # cython.int



def test_carray_setcomp_pointer_int_2_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_int_2_pointer())
    [0]
    """
    carray: cython.pointer[cython.int] = [0, 0]

    return {item for item in carray[:2]}  # cython.int



def test_carray_genexpr_pointer_int_2_pointer():
    """
    >>> list(test_carray_genexpr_pointer_int_2_pointer())
    [0, 0]
    """
    carray: cython.pointer[cython.int] = [0, 0]

    return (item for item in carray[:2])  # cython.int



def test_carray_forin_constant_int_4_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_int_4_constant_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.int[5] = [1, 2, 3, 4, arg]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_4_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_int_4_constant_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.int[5] = [1, 2, 3, 4, arg]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_4_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_int_4_constant_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.int[5] = [1, 2, 3, 4, arg]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_4_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_int_4_constant_arg(4))
    [1, 2, 3, 4]
    """
    carray: cython.int[5] = [1, 2, 3, 4, arg]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_4_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_int_4_constant_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.int[5] = [1, 2, 3, 4, arg]

    return (item for item in carray)  # cython.int



def test_carray_forin_constant_int_4_constant():
    """
    >>> test_carray_forin_constant_int_4_constant()
    [1, 2, 3, 4]
    """
    carray: cython.int[4] = [1, 2, 3, 4]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_4_constant():
    """
    >>> list(test_carray_generator_constant_int_4_constant())
    [1, 2, 3, 4]
    """
    carray: cython.int[4] = [1, 2, 3, 4]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_4_constant():
    """
    >>> test_carray_listcomp_constant_int_4_constant()
    [1, 2, 3, 4]
    """
    carray: cython.int[4] = [1, 2, 3, 4]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_4_constant():
    """
    >>> sorted(test_carray_setcomp_constant_int_4_constant())
    [1, 2, 3, 4]
    """
    carray: cython.int[4] = [1, 2, 3, 4]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_4_constant():
    """
    >>> list(test_carray_genexpr_constant_int_4_constant())
    [1, 2, 3, 4]
    """
    carray: cython.int[4] = [1, 2, 3, 4]

    return (item for item in carray)  # cython.int



def test_literal_forin_literal_int_4_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_int_4_literal_arg(4)
    [1, 2, 3, 4, 4]
    """


    items = []
    for item in [1, 2, 3, 4, arg]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_4_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_int_4_literal_arg(4))
    [1, 2, 3, 4, 4]
    """


    for item in [1, 2, 3, 4, arg]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_4_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_int_4_literal_arg(4)
    [1, 2, 3, 4, 4]
    """


    return [item for item in [1, 2, 3, 4, arg]]  # cython.int



def test_literal_setcomp_literal_int_4_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_int_4_literal_arg(4))
    [1, 2, 3, 4]
    """


    return {item for item in [1, 2, 3, 4, arg]}  # cython.int



def test_literal_genexpr_literal_int_4_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_int_4_literal_arg(4))
    [1, 2, 3, 4, 4]
    """


    return (item for item in [1, 2, 3, 4, arg])  # cython.int



def test_literal_forin_literal_int_4_literal():
    """
    >>> test_literal_forin_literal_int_4_literal()
    [1, 2, 3, 4]
    """


    items = []
    for item in [1, 2, 3, 4]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_4_literal():
    """
    >>> list(test_literal_generator_literal_int_4_literal())
    [1, 2, 3, 4]
    """


    for item in [1, 2, 3, 4]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_4_literal():
    """
    >>> test_literal_listcomp_literal_int_4_literal()
    [1, 2, 3, 4]
    """


    return [item for item in [1, 2, 3, 4]]  # cython.int



def test_literal_setcomp_literal_int_4_literal():
    """
    >>> sorted(test_literal_setcomp_literal_int_4_literal())
    [1, 2, 3, 4]
    """


    return {item for item in [1, 2, 3, 4]}  # cython.int



def test_literal_genexpr_literal_int_4_literal():
    """
    >>> list(test_literal_genexpr_literal_int_4_literal())
    [1, 2, 3, 4]
    """


    return (item for item in [1, 2, 3, 4])  # cython.int



def test_carray_forin_pointer_int_4_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_int_4_pointer_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4, arg]

    items = []
    for item in carray[:5]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_4_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_int_4_pointer_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4, arg]

    for item in carray[:5]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_4_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_int_4_pointer_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4, arg]

    return [item for item in carray[:5]]  # cython.int



def test_carray_setcomp_pointer_int_4_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_int_4_pointer_arg(4))
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4, arg]

    return {item for item in carray[:5]}  # cython.int



def test_carray_genexpr_pointer_int_4_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_int_4_pointer_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4, arg]

    return (item for item in carray[:5])  # cython.int



def test_carray_forin_pointer_int_4_pointer():
    """
    >>> test_carray_forin_pointer_int_4_pointer()
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4]

    items = []
    for item in carray[:4]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_4_pointer():
    """
    >>> list(test_carray_generator_pointer_int_4_pointer())
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4]

    for item in carray[:4]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_4_pointer():
    """
    >>> test_carray_listcomp_pointer_int_4_pointer()
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4]

    return [item for item in carray[:4]]  # cython.int



def test_carray_setcomp_pointer_int_4_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_int_4_pointer())
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4]

    return {item for item in carray[:4]}  # cython.int



def test_carray_genexpr_pointer_int_4_pointer():
    """
    >>> list(test_carray_genexpr_pointer_int_4_pointer())
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.int] = [1, 2, 3, 4]

    return (item for item in carray[:4])  # cython.int



def test_carray_forin_constant_int_266_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_int_266_constant_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.int[267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_266_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_int_266_constant_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.int[267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_266_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_int_266_constant_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.int[267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_266_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_int_266_constant_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.int[267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_266_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_int_266_constant_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.int[267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return (item for item in carray)  # cython.int



def test_carray_forin_constant_int_266_constant():
    """
    >>> test_carray_forin_constant_int_266_constant()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.int[266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items



def test_carray_generator_constant_int_266_constant():
    """
    >>> list(test_carray_generator_constant_int_266_constant())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.int[266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    for item in carray:  # cython.int
        yield item



def test_carray_listcomp_constant_int_266_constant():
    """
    >>> test_carray_listcomp_constant_int_266_constant()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.int[266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return [item for item in carray]  # cython.int



def test_carray_setcomp_constant_int_266_constant():
    """
    >>> sorted(test_carray_setcomp_constant_int_266_constant())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.int[266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return {item for item in carray}  # cython.int



def test_carray_genexpr_constant_int_266_constant():
    """
    >>> list(test_carray_genexpr_constant_int_266_constant())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.int[266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return (item for item in carray)  # cython.int



def test_literal_forin_literal_int_266_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_int_266_literal_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    items = []
    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_266_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_int_266_literal_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_266_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_int_266_literal_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    return [item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]]  # cython.int



def test_literal_setcomp_literal_int_266_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_int_266_literal_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return {item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]}  # cython.int



def test_literal_genexpr_literal_int_266_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_int_266_literal_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    return (item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg])  # cython.int



def test_literal_forin_literal_int_266_literal():
    """
    >>> test_literal_forin_literal_int_266_literal()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    items = []
    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]:  # cython.int
        items.append(item)
    return items



def test_literal_generator_literal_int_266_literal():
    """
    >>> list(test_literal_generator_literal_int_266_literal())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]:  # cython.int
        yield item



def test_literal_listcomp_literal_int_266_literal():
    """
    >>> test_literal_listcomp_literal_int_266_literal()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return [item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]]  # cython.int



def test_literal_setcomp_literal_int_266_literal():
    """
    >>> sorted(test_literal_setcomp_literal_int_266_literal())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return {item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]}  # cython.int



def test_literal_genexpr_literal_int_266_literal():
    """
    >>> list(test_literal_genexpr_literal_int_266_literal())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return (item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])  # cython.int



def test_carray_forin_pointer_int_266_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_int_266_pointer_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    items = []
    for item in carray[:267]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_266_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_int_266_pointer_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    for item in carray[:267]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_266_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_int_266_pointer_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return [item for item in carray[:267]]  # cython.int



def test_carray_setcomp_pointer_int_266_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_int_266_pointer_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return {item for item in carray[:267]}  # cython.int



def test_carray_genexpr_pointer_int_266_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_int_266_pointer_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return (item for item in carray[:267])  # cython.int



def test_carray_forin_pointer_int_266_pointer():
    """
    >>> test_carray_forin_pointer_int_266_pointer()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    items = []
    for item in carray[:266]:  # cython.int
        items.append(item)
    return items



def test_carray_generator_pointer_int_266_pointer():
    """
    >>> list(test_carray_generator_pointer_int_266_pointer())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    for item in carray[:266]:  # cython.int
        yield item



def test_carray_listcomp_pointer_int_266_pointer():
    """
    >>> test_carray_listcomp_pointer_int_266_pointer()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return [item for item in carray[:266]]  # cython.int



def test_carray_setcomp_pointer_int_266_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_int_266_pointer())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return {item for item in carray[:266]}  # cython.int



def test_carray_genexpr_pointer_int_266_pointer():
    """
    >>> list(test_carray_genexpr_pointer_int_266_pointer())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.int] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return (item for item in carray[:266])  # cython.int



def test_carray_forin_constant_const_int_1_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_const_int_1_constant_arg(4)
    [0, 4]
    """
    carray: cython.const[cython.int][2] = [0, arg]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_1_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_const_int_1_constant_arg(4))
    [0, 4]
    """
    carray: cython.const[cython.int][2] = [0, arg]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_1_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_const_int_1_constant_arg(4)
    [0, 4]
    """
    carray: cython.const[cython.int][2] = [0, arg]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_1_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_const_int_1_constant_arg(4))
    [0, 4]
    """
    carray: cython.const[cython.int][2] = [0, arg]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_1_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_const_int_1_constant_arg(4))
    [0, 4]
    """
    carray: cython.const[cython.int][2] = [0, arg]

    return (item for item in carray)  # cython.const[cython.int]



def test_carray_forin_constant_const_int_1_constant():
    """
    >>> test_carray_forin_constant_const_int_1_constant()
    [0]
    """
    carray: cython.const[cython.int][1] = [0]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_1_constant():
    """
    >>> list(test_carray_generator_constant_const_int_1_constant())
    [0]
    """
    carray: cython.const[cython.int][1] = [0]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_1_constant():
    """
    >>> test_carray_listcomp_constant_const_int_1_constant()
    [0]
    """
    carray: cython.const[cython.int][1] = [0]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_int_1_constant())
    [0]
    """
    carray: cython.const[cython.int][1] = [0]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_1_constant():
    """
    >>> list(test_carray_genexpr_constant_const_int_1_constant())
    [0]
    """
    carray: cython.const[cython.int][1] = [0]

    return (item for item in carray)  # cython.const[cython.int]



def test_literal_forin_literal_const_int_1_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_const_int_1_literal_arg(4)
    [0, 4]
    """


    items = []
    for item in [0, arg]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_1_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_const_int_1_literal_arg(4))
    [0, 4]
    """


    for item in [0, arg]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_1_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_const_int_1_literal_arg(4)
    [0, 4]
    """


    return [item for item in [0, arg]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_1_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_const_int_1_literal_arg(4))
    [0, 4]
    """


    return {item for item in [0, arg]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_1_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_const_int_1_literal_arg(4))
    [0, 4]
    """


    return (item for item in [0, arg])  # cython.const[cython.int]



def test_literal_forin_literal_const_int_1_literal():
    """
    >>> test_literal_forin_literal_const_int_1_literal()
    [0]
    """


    items = []
    for item in [0]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_1_literal():
    """
    >>> list(test_literal_generator_literal_const_int_1_literal())
    [0]
    """


    for item in [0]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_1_literal():
    """
    >>> test_literal_listcomp_literal_const_int_1_literal()
    [0]
    """


    return [item for item in [0]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_int_1_literal())
    [0]
    """


    return {item for item in [0]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_1_literal():
    """
    >>> list(test_literal_genexpr_literal_const_int_1_literal())
    [0]
    """


    return (item for item in [0])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_1_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_const_int_1_pointer_arg(4)
    [0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, arg]

    items = []
    for item in carray[:2]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_1_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_const_int_1_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, arg]

    for item in carray[:2]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_1_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_const_int_1_pointer_arg(4)
    [0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, arg]

    return [item for item in carray[:2]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_1_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_1_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, arg]

    return {item for item in carray[:2]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_1_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_const_int_1_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, arg]

    return (item for item in carray[:2])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_1_pointer():
    """
    >>> test_carray_forin_pointer_const_int_1_pointer()
    [0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0]

    items = []
    for item in carray[:1]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_1_pointer():
    """
    >>> list(test_carray_generator_pointer_const_int_1_pointer())
    [0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0]

    for item in carray[:1]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_1_pointer():
    """
    >>> test_carray_listcomp_pointer_const_int_1_pointer()
    [0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0]

    return [item for item in carray[:1]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_1_pointer())
    [0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0]

    return {item for item in carray[:1]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_int_1_pointer())
    [0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0]

    return (item for item in carray[:1])  # cython.const[cython.int]



def test_carray_forin_constant_const_int_2_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_const_int_2_constant_arg(4)
    [0, 0, 4]
    """
    carray: cython.const[cython.int][3] = [0, 0, arg]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_2_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_const_int_2_constant_arg(4))
    [0, 0, 4]
    """
    carray: cython.const[cython.int][3] = [0, 0, arg]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_2_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_const_int_2_constant_arg(4)
    [0, 0, 4]
    """
    carray: cython.const[cython.int][3] = [0, 0, arg]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_2_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_const_int_2_constant_arg(4))
    [0, 4]
    """
    carray: cython.const[cython.int][3] = [0, 0, arg]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_2_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_const_int_2_constant_arg(4))
    [0, 0, 4]
    """
    carray: cython.const[cython.int][3] = [0, 0, arg]

    return (item for item in carray)  # cython.const[cython.int]



def test_carray_forin_constant_const_int_2_constant():
    """
    >>> test_carray_forin_constant_const_int_2_constant()
    [0, 0]
    """
    carray: cython.const[cython.int][2] = [0, 0]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_2_constant():
    """
    >>> list(test_carray_generator_constant_const_int_2_constant())
    [0, 0]
    """
    carray: cython.const[cython.int][2] = [0, 0]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_2_constant():
    """
    >>> test_carray_listcomp_constant_const_int_2_constant()
    [0, 0]
    """
    carray: cython.const[cython.int][2] = [0, 0]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_2_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_int_2_constant())
    [0]
    """
    carray: cython.const[cython.int][2] = [0, 0]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_2_constant():
    """
    >>> list(test_carray_genexpr_constant_const_int_2_constant())
    [0, 0]
    """
    carray: cython.const[cython.int][2] = [0, 0]

    return (item for item in carray)  # cython.const[cython.int]



def test_literal_forin_literal_const_int_2_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_const_int_2_literal_arg(4)
    [0, 0, 4]
    """


    items = []
    for item in [0, 0, arg]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_2_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_const_int_2_literal_arg(4))
    [0, 0, 4]
    """


    for item in [0, 0, arg]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_2_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_const_int_2_literal_arg(4)
    [0, 0, 4]
    """


    return [item for item in [0, 0, arg]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_2_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_const_int_2_literal_arg(4))
    [0, 4]
    """


    return {item for item in [0, 0, arg]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_2_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_const_int_2_literal_arg(4))
    [0, 0, 4]
    """


    return (item for item in [0, 0, arg])  # cython.const[cython.int]



def test_literal_forin_literal_const_int_2_literal():
    """
    >>> test_literal_forin_literal_const_int_2_literal()
    [0, 0]
    """


    items = []
    for item in [0, 0]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_2_literal():
    """
    >>> list(test_literal_generator_literal_const_int_2_literal())
    [0, 0]
    """


    for item in [0, 0]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_2_literal():
    """
    >>> test_literal_listcomp_literal_const_int_2_literal()
    [0, 0]
    """


    return [item for item in [0, 0]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_2_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_int_2_literal())
    [0]
    """


    return {item for item in [0, 0]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_2_literal():
    """
    >>> list(test_literal_genexpr_literal_const_int_2_literal())
    [0, 0]
    """


    return (item for item in [0, 0])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_2_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_const_int_2_pointer_arg(4)
    [0, 0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0, arg]

    items = []
    for item in carray[:3]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_2_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_const_int_2_pointer_arg(4))
    [0, 0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0, arg]

    for item in carray[:3]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_2_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_const_int_2_pointer_arg(4)
    [0, 0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0, arg]

    return [item for item in carray[:3]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_2_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_2_pointer_arg(4))
    [0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0, arg]

    return {item for item in carray[:3]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_2_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_const_int_2_pointer_arg(4))
    [0, 0, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0, arg]

    return (item for item in carray[:3])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_2_pointer():
    """
    >>> test_carray_forin_pointer_const_int_2_pointer()
    [0, 0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0]

    items = []
    for item in carray[:2]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_2_pointer():
    """
    >>> list(test_carray_generator_pointer_const_int_2_pointer())
    [0, 0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0]

    for item in carray[:2]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_2_pointer():
    """
    >>> test_carray_listcomp_pointer_const_int_2_pointer()
    [0, 0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0]

    return [item for item in carray[:2]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_2_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_2_pointer())
    [0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0]

    return {item for item in carray[:2]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_2_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_int_2_pointer())
    [0, 0]
    """
    carray: cython.pointer[cython.const[cython.int]] = [0, 0]

    return (item for item in carray[:2])  # cython.const[cython.int]



def test_carray_forin_constant_const_int_4_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_const_int_4_constant_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.const[cython.int][5] = [1, 2, 3, 4, arg]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_4_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_const_int_4_constant_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.const[cython.int][5] = [1, 2, 3, 4, arg]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_4_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_const_int_4_constant_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.const[cython.int][5] = [1, 2, 3, 4, arg]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_4_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_const_int_4_constant_arg(4))
    [1, 2, 3, 4]
    """
    carray: cython.const[cython.int][5] = [1, 2, 3, 4, arg]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_4_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_const_int_4_constant_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.const[cython.int][5] = [1, 2, 3, 4, arg]

    return (item for item in carray)  # cython.const[cython.int]



def test_carray_forin_constant_const_int_4_constant():
    """
    >>> test_carray_forin_constant_const_int_4_constant()
    [1, 2, 3, 4]
    """
    carray: cython.const[cython.int][4] = [1, 2, 3, 4]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_4_constant():
    """
    >>> list(test_carray_generator_constant_const_int_4_constant())
    [1, 2, 3, 4]
    """
    carray: cython.const[cython.int][4] = [1, 2, 3, 4]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_4_constant():
    """
    >>> test_carray_listcomp_constant_const_int_4_constant()
    [1, 2, 3, 4]
    """
    carray: cython.const[cython.int][4] = [1, 2, 3, 4]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_4_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_int_4_constant())
    [1, 2, 3, 4]
    """
    carray: cython.const[cython.int][4] = [1, 2, 3, 4]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_4_constant():
    """
    >>> list(test_carray_genexpr_constant_const_int_4_constant())
    [1, 2, 3, 4]
    """
    carray: cython.const[cython.int][4] = [1, 2, 3, 4]

    return (item for item in carray)  # cython.const[cython.int]



def test_literal_forin_literal_const_int_4_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_const_int_4_literal_arg(4)
    [1, 2, 3, 4, 4]
    """


    items = []
    for item in [1, 2, 3, 4, arg]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_4_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_const_int_4_literal_arg(4))
    [1, 2, 3, 4, 4]
    """


    for item in [1, 2, 3, 4, arg]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_4_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_const_int_4_literal_arg(4)
    [1, 2, 3, 4, 4]
    """


    return [item for item in [1, 2, 3, 4, arg]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_4_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_const_int_4_literal_arg(4))
    [1, 2, 3, 4]
    """


    return {item for item in [1, 2, 3, 4, arg]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_4_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_const_int_4_literal_arg(4))
    [1, 2, 3, 4, 4]
    """


    return (item for item in [1, 2, 3, 4, arg])  # cython.const[cython.int]



def test_literal_forin_literal_const_int_4_literal():
    """
    >>> test_literal_forin_literal_const_int_4_literal()
    [1, 2, 3, 4]
    """


    items = []
    for item in [1, 2, 3, 4]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_4_literal():
    """
    >>> list(test_literal_generator_literal_const_int_4_literal())
    [1, 2, 3, 4]
    """


    for item in [1, 2, 3, 4]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_4_literal():
    """
    >>> test_literal_listcomp_literal_const_int_4_literal()
    [1, 2, 3, 4]
    """


    return [item for item in [1, 2, 3, 4]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_4_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_int_4_literal())
    [1, 2, 3, 4]
    """


    return {item for item in [1, 2, 3, 4]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_4_literal():
    """
    >>> list(test_literal_genexpr_literal_const_int_4_literal())
    [1, 2, 3, 4]
    """


    return (item for item in [1, 2, 3, 4])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_4_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_const_int_4_pointer_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4, arg]

    items = []
    for item in carray[:5]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_4_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_const_int_4_pointer_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4, arg]

    for item in carray[:5]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_4_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_const_int_4_pointer_arg(4)
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4, arg]

    return [item for item in carray[:5]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_4_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_4_pointer_arg(4))
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4, arg]

    return {item for item in carray[:5]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_4_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_const_int_4_pointer_arg(4))
    [1, 2, 3, 4, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4, arg]

    return (item for item in carray[:5])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_4_pointer():
    """
    >>> test_carray_forin_pointer_const_int_4_pointer()
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4]

    items = []
    for item in carray[:4]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_4_pointer():
    """
    >>> list(test_carray_generator_pointer_const_int_4_pointer())
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4]

    for item in carray[:4]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_4_pointer():
    """
    >>> test_carray_listcomp_pointer_const_int_4_pointer()
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4]

    return [item for item in carray[:4]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_4_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_4_pointer())
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4]

    return {item for item in carray[:4]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_4_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_int_4_pointer())
    [1, 2, 3, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [1, 2, 3, 4]

    return (item for item in carray[:4])  # cython.const[cython.int]



def test_carray_forin_constant_const_int_266_constant_arg(arg: cython.int):
    """
    >>> test_carray_forin_constant_const_int_266_constant_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.const[cython.int][267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_266_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_constant_const_int_266_constant_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.const[cython.int][267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_266_constant_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_constant_const_int_266_constant_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.const[cython.int][267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_266_constant_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_constant_const_int_266_constant_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.const[cython.int][267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_266_constant_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_constant_const_int_266_constant_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.const[cython.int][267] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return (item for item in carray)  # cython.const[cython.int]



def test_carray_forin_constant_const_int_266_constant():
    """
    >>> test_carray_forin_constant_const_int_266_constant()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.const[cython.int][266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    items = []
    for item in carray:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_constant_const_int_266_constant():
    """
    >>> list(test_carray_generator_constant_const_int_266_constant())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.const[cython.int][266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    for item in carray:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_constant_const_int_266_constant():
    """
    >>> test_carray_listcomp_constant_const_int_266_constant()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.const[cython.int][266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return [item for item in carray]  # cython.const[cython.int]



def test_carray_setcomp_constant_const_int_266_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_int_266_constant())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.const[cython.int][266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return {item for item in carray}  # cython.const[cython.int]



def test_carray_genexpr_constant_const_int_266_constant():
    """
    >>> list(test_carray_genexpr_constant_const_int_266_constant())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.const[cython.int][266] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return (item for item in carray)  # cython.const[cython.int]



def test_literal_forin_literal_const_int_266_literal_arg(arg: cython.int):
    """
    >>> test_literal_forin_literal_const_int_266_literal_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    items = []
    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_266_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_generator_literal_const_int_266_literal_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_266_literal_arg(arg: cython.int):
    """
    >>> test_literal_listcomp_literal_const_int_266_literal_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    return [item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_266_literal_arg(arg: cython.int):
    """
    >>> sorted(test_literal_setcomp_literal_const_int_266_literal_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return {item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_266_literal_arg(arg: cython.int):
    """
    >>> list(test_literal_genexpr_literal_const_int_266_literal_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """


    return (item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg])  # cython.const[cython.int]



def test_literal_forin_literal_const_int_266_literal():
    """
    >>> test_literal_forin_literal_const_int_266_literal()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    items = []
    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_literal_generator_literal_const_int_266_literal():
    """
    >>> list(test_literal_generator_literal_const_int_266_literal())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]:  # cython.const[cython.int]
        yield item



def test_literal_listcomp_literal_const_int_266_literal():
    """
    >>> test_literal_listcomp_literal_const_int_266_literal()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return [item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]]  # cython.const[cython.int]



def test_literal_setcomp_literal_const_int_266_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_int_266_literal())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return {item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]}  # cython.const[cython.int]



def test_literal_genexpr_literal_const_int_266_literal():
    """
    >>> list(test_literal_genexpr_literal_const_int_266_literal())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """


    return (item for item in [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_266_pointer_arg(arg: cython.int):
    """
    >>> test_carray_forin_pointer_const_int_266_pointer_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    items = []
    for item in carray[:267]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_266_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_generator_pointer_const_int_266_pointer_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    for item in carray[:267]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_266_pointer_arg(arg: cython.int):
    """
    >>> test_carray_listcomp_pointer_const_int_266_pointer_arg(4)
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return [item for item in carray[:267]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_266_pointer_arg(arg: cython.int):
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_266_pointer_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return {item for item in carray[:267]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_266_pointer_arg(arg: cython.int):
    """
    >>> list(test_carray_genexpr_pointer_const_int_266_pointer_arg(4))
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 4]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, arg]

    return (item for item in carray[:267])  # cython.const[cython.int]



def test_carray_forin_pointer_const_int_266_pointer():
    """
    >>> test_carray_forin_pointer_const_int_266_pointer()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    items = []
    for item in carray[:266]:  # cython.const[cython.int]
        items.append(item)
    return items



def test_carray_generator_pointer_const_int_266_pointer():
    """
    >>> list(test_carray_generator_pointer_const_int_266_pointer())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    for item in carray[:266]:  # cython.const[cython.int]
        yield item



def test_carray_listcomp_pointer_const_int_266_pointer():
    """
    >>> test_carray_listcomp_pointer_const_int_266_pointer()
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return [item for item in carray[:266]]  # cython.const[cython.int]



def test_carray_setcomp_pointer_const_int_266_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_int_266_pointer())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return {item for item in carray[:266]}  # cython.const[cython.int]



def test_carray_genexpr_pointer_const_int_266_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_int_266_pointer())
    [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]
    """
    carray: cython.pointer[cython.const[cython.int]] = [-133, -132, -131, -130, -129, -128, -127, -126, -125, -124, -123, -122, -121, -120, -119, -118, -117, -116, -115, -114, -113, -112, -111, -110, -109, -108, -107, -106, -105, -104, -103, -102, -101, -100, -99, -98, -97, -96, -95, -94, -93, -92, -91, -90, -89, -88, -87, -86, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -74, -73, -72, -71, -70, -69, -68, -67, -66, -65, -64, -63, -62, -61, -60, -59, -58, -57, -56, -55, -54, -53, -52, -51, -50, -49, -48, -47, -46, -45, -44, -43, -42, -41, -40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132]

    return (item for item in carray[:266])  # cython.const[cython.int]



def test_carray_forin_constant_char_1_constant():
    """
    >>> test_carray_forin_constant_char_1_constant()
    [120]
    """
    carray: cython.char[1] = b'x'

    items = []
    for item in carray:  # cython.char
        items.append(item)
    return items



def test_carray_generator_constant_char_1_constant():
    """
    >>> list(test_carray_generator_constant_char_1_constant())
    [120]
    """
    carray: cython.char[1] = b'x'

    for item in carray:  # cython.char
        yield item



def test_carray_listcomp_constant_char_1_constant():
    """
    >>> test_carray_listcomp_constant_char_1_constant()
    [120]
    """
    carray: cython.char[1] = b'x'

    return [item for item in carray]  # cython.char



def test_carray_setcomp_constant_char_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_char_1_constant())
    [120]
    """
    carray: cython.char[1] = b'x'

    return {item for item in carray}  # cython.char



def test_carray_genexpr_constant_char_1_constant():
    """
    >>> list(test_carray_genexpr_constant_char_1_constant())
    [120]
    """
    carray: cython.char[1] = b'x'

    return (item for item in carray)  # cython.char



def test_literal_forin_literal_char_1_literal():
    """
    >>> test_literal_forin_literal_char_1_literal()
    [120]
    """


    items = []
    for item in b'x':  # cython.char
        items.append(item)
    return items



def test_literal_generator_literal_char_1_literal():
    """
    >>> list(test_literal_generator_literal_char_1_literal())
    [120]
    """


    for item in b'x':  # cython.char
        yield item



def test_literal_listcomp_literal_char_1_literal():
    """
    >>> test_literal_listcomp_literal_char_1_literal()
    [120]
    """


    return [item for item in b'x']  # cython.char



def test_literal_setcomp_literal_char_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_char_1_literal())
    [120]
    """


    return {item for item in b'x'}  # cython.char



def test_literal_genexpr_literal_char_1_literal():
    """
    >>> list(test_literal_genexpr_literal_char_1_literal())
    [120]
    """


    return (item for item in b'x')  # cython.char



def test_carray_forin_pointer_char_1_pointer():
    """
    >>> test_carray_forin_pointer_char_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.char] = b'x'

    items = []
    for item in carray[:1]:  # cython.char
        items.append(item)
    return items



def test_carray_generator_pointer_char_1_pointer():
    """
    >>> list(test_carray_generator_pointer_char_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.char] = b'x'

    for item in carray[:1]:  # cython.char
        yield item



def test_carray_listcomp_pointer_char_1_pointer():
    """
    >>> test_carray_listcomp_pointer_char_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.char] = b'x'

    return [item for item in carray[:1]]  # cython.char



def test_carray_setcomp_pointer_char_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_char_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.char] = b'x'

    return {item for item in carray[:1]}  # cython.char



def test_carray_genexpr_pointer_char_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_char_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.char] = b'x'

    return (item for item in carray[:1])  # cython.char



def test_carray_forin_constant_char_7_constant():
    """
    >>> test_carray_forin_constant_char_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.char[7] = b'abcdefg'

    items = []
    for item in carray:  # cython.char
        items.append(item)
    return items



def test_carray_generator_constant_char_7_constant():
    """
    >>> list(test_carray_generator_constant_char_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.char[7] = b'abcdefg'

    for item in carray:  # cython.char
        yield item



def test_carray_listcomp_constant_char_7_constant():
    """
    >>> test_carray_listcomp_constant_char_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.char[7] = b'abcdefg'

    return [item for item in carray]  # cython.char



def test_carray_setcomp_constant_char_7_constant():
    """
    >>> sorted(test_carray_setcomp_constant_char_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.char[7] = b'abcdefg'

    return {item for item in carray}  # cython.char



def test_carray_genexpr_constant_char_7_constant():
    """
    >>> list(test_carray_genexpr_constant_char_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.char[7] = b'abcdefg'

    return (item for item in carray)  # cython.char



def test_literal_forin_literal_char_7_literal():
    """
    >>> test_literal_forin_literal_char_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    items = []
    for item in b'abcdefg':  # cython.char
        items.append(item)
    return items



def test_literal_generator_literal_char_7_literal():
    """
    >>> list(test_literal_generator_literal_char_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    for item in b'abcdefg':  # cython.char
        yield item



def test_literal_listcomp_literal_char_7_literal():
    """
    >>> test_literal_listcomp_literal_char_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    return [item for item in b'abcdefg']  # cython.char



def test_literal_setcomp_literal_char_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_char_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return {item for item in b'abcdefg'}  # cython.char



def test_literal_genexpr_literal_char_7_literal():
    """
    >>> list(test_literal_genexpr_literal_char_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return (item for item in b'abcdefg')  # cython.char



def test_carray_forin_pointer_char_7_pointer():
    """
    >>> test_carray_forin_pointer_char_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.char] = b'abcdefg'

    items = []
    for item in carray[:7]:  # cython.char
        items.append(item)
    return items



def test_carray_generator_pointer_char_7_pointer():
    """
    >>> list(test_carray_generator_pointer_char_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.char] = b'abcdefg'

    for item in carray[:7]:  # cython.char
        yield item



def test_carray_listcomp_pointer_char_7_pointer():
    """
    >>> test_carray_listcomp_pointer_char_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.char] = b'abcdefg'

    return [item for item in carray[:7]]  # cython.char



def test_carray_setcomp_pointer_char_7_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_char_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.char] = b'abcdefg'

    return {item for item in carray[:7]}  # cython.char



def test_carray_genexpr_pointer_char_7_pointer():
    """
    >>> list(test_carray_genexpr_pointer_char_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.char] = b'abcdefg'

    return (item for item in carray[:7])  # cython.char



def test_carray_forin_constant_char_100_constant():
    """
    >>> test_carray_forin_constant_char_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.char[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray:  # cython.char
        items.append(item)
    return items



def test_carray_generator_constant_char_100_constant():
    """
    >>> list(test_carray_generator_constant_char_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.char[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray:  # cython.char
        yield item



def test_carray_listcomp_constant_char_100_constant():
    """
    >>> test_carray_listcomp_constant_char_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.char[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray]  # cython.char



def test_carray_setcomp_constant_char_100_constant():
    """
    >>> sorted(test_carray_setcomp_constant_char_100_constant())
    [120]
    """
    carray: cython.char[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray}  # cython.char



def test_carray_genexpr_constant_char_100_constant():
    """
    >>> list(test_carray_genexpr_constant_char_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.char[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray)  # cython.char



def test_literal_forin_literal_char_100_literal():
    """
    >>> test_literal_forin_literal_char_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    items = []
    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.char
        items.append(item)
    return items



def test_literal_generator_literal_char_100_literal():
    """
    >>> list(test_literal_generator_literal_char_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.char
        yield item



def test_literal_listcomp_literal_char_100_literal():
    """
    >>> test_literal_listcomp_literal_char_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return [item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']  # cython.char



def test_literal_setcomp_literal_char_100_literal():
    """
    >>> sorted(test_literal_setcomp_literal_char_100_literal())
    [120]
    """


    return {item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}  # cython.char



def test_literal_genexpr_literal_char_100_literal():
    """
    >>> list(test_literal_genexpr_literal_char_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return (item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # cython.char



def test_carray_forin_pointer_char_100_pointer():
    """
    >>> test_carray_forin_pointer_char_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.char] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray[:100]:  # cython.char
        items.append(item)
    return items



def test_carray_generator_pointer_char_100_pointer():
    """
    >>> list(test_carray_generator_pointer_char_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.char] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray[:100]:  # cython.char
        yield item



def test_carray_listcomp_pointer_char_100_pointer():
    """
    >>> test_carray_listcomp_pointer_char_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.char] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray[:100]]  # cython.char



def test_carray_setcomp_pointer_char_100_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_char_100_pointer())
    [120]
    """
    carray: cython.pointer[cython.char] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray[:100]}  # cython.char



def test_carray_genexpr_pointer_char_100_pointer():
    """
    >>> list(test_carray_genexpr_pointer_char_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.char] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray[:100])  # cython.char



def test_carray_forin_constant_char_1_11_constant():
    """
    >>> charlist(test_carray_forin_constant_char_1_11_constant())
    [88]
    """
    carray: cython.char[1] = 'X'

    items = []
    for item in carray:  # cython.char
        items.append(item)
    return items



def test_carray_generator_constant_char_1_11_constant():
    """
    >>> charlist(list(test_carray_generator_constant_char_1_11_constant()))
    [88]
    """
    carray: cython.char[1] = 'X'

    for item in carray:  # cython.char
        yield item



def test_carray_listcomp_constant_char_1_11_constant():
    """
    >>> charlist(test_carray_listcomp_constant_char_1_11_constant())
    [88]
    """
    carray: cython.char[1] = 'X'

    return [item for item in carray]  # cython.char



def test_carray_setcomp_constant_char_1_11_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_char_1_11_constant()))
    [88]
    """
    carray: cython.char[1] = 'X'

    return {item for item in carray}  # cython.char



def test_carray_genexpr_constant_char_1_11_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_char_1_11_constant()))
    [88]
    """
    carray: cython.char[1] = 'X'

    return (item for item in carray)  # cython.char



def test_literal_forin_literal_char_1_11_literal():
    """
    >>> test_literal_forin_literal_char_1_11_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.char
        items.append(item)
    return items



def test_literal_generator_literal_char_1_11_literal():
    """
    >>> list(test_literal_generator_literal_char_1_11_literal())
    ['X']
    """


    for item in 'X':  # cython.char
        yield item



def test_literal_listcomp_literal_char_1_11_literal():
    """
    >>> test_literal_listcomp_literal_char_1_11_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.char



def test_literal_setcomp_literal_char_1_11_literal():
    """
    >>> sorted(test_literal_setcomp_literal_char_1_11_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.char



def test_literal_genexpr_literal_char_1_11_literal():
    """
    >>> list(test_literal_genexpr_literal_char_1_11_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.char



def test_carray_forin_pointer_char_1_11_pointer():
    """
    >>> charlist(test_carray_forin_pointer_char_1_11_pointer())
    [88]
    """
    carray: cython.pointer[cython.char] = 'X'

    items = []
    for item in carray[:1]:  # cython.char
        items.append(item)
    return items



def test_carray_generator_pointer_char_1_11_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_char_1_11_pointer()))
    [88]
    """
    carray: cython.pointer[cython.char] = 'X'

    for item in carray[:1]:  # cython.char
        yield item



def test_carray_listcomp_pointer_char_1_11_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_char_1_11_pointer())
    [88]
    """
    carray: cython.pointer[cython.char] = 'X'

    return [item for item in carray[:1]]  # cython.char



def test_carray_setcomp_pointer_char_1_11_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_char_1_11_pointer()))
    [88]
    """
    carray: cython.pointer[cython.char] = 'X'

    return {item for item in carray[:1]}  # cython.char



def test_carray_genexpr_pointer_char_1_11_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_char_1_11_pointer()))
    [88]
    """
    carray: cython.pointer[cython.char] = 'X'

    return (item for item in carray[:1])  # cython.char



def test_carray_forin_constant_char_7_12_constant():
    """
    >>> charlist(test_carray_forin_constant_char_7_12_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.char[7] = 'abc-def'

    items = []
    for item in carray:  # cython.char
        items.append(item)
    return items



def test_carray_generator_constant_char_7_12_constant():
    """
    >>> charlist(list(test_carray_generator_constant_char_7_12_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.char[7] = 'abc-def'

    for item in carray:  # cython.char
        yield item



def test_carray_listcomp_constant_char_7_12_constant():
    """
    >>> charlist(test_carray_listcomp_constant_char_7_12_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.char[7] = 'abc-def'

    return [item for item in carray]  # cython.char



def test_carray_setcomp_constant_char_7_12_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_char_7_12_constant()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.char[7] = 'abc-def'

    return {item for item in carray}  # cython.char



def test_carray_genexpr_constant_char_7_12_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_char_7_12_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.char[7] = 'abc-def'

    return (item for item in carray)  # cython.char



def test_literal_forin_literal_char_7_12_literal():
    """
    >>> test_literal_forin_literal_char_7_12_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.char
        items.append(item)
    return items



def test_literal_generator_literal_char_7_12_literal():
    """
    >>> list(test_literal_generator_literal_char_7_12_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.char
        yield item



def test_literal_listcomp_literal_char_7_12_literal():
    """
    >>> test_literal_listcomp_literal_char_7_12_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.char



def test_literal_setcomp_literal_char_7_12_literal():
    """
    >>> sorted(test_literal_setcomp_literal_char_7_12_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.char



def test_literal_genexpr_literal_char_7_12_literal():
    """
    >>> list(test_literal_genexpr_literal_char_7_12_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.char



def test_carray_forin_pointer_char_7_12_pointer():
    """
    >>> charlist(test_carray_forin_pointer_char_7_12_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.char] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.char
        items.append(item)
    return items



def test_carray_generator_pointer_char_7_12_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_char_7_12_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.char] = 'abc-def'

    for item in carray[:7]:  # cython.char
        yield item



def test_carray_listcomp_pointer_char_7_12_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_char_7_12_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.char] = 'abc-def'

    return [item for item in carray[:7]]  # cython.char



def test_carray_setcomp_pointer_char_7_12_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_char_7_12_pointer()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.pointer[cython.char] = 'abc-def'

    return {item for item in carray[:7]}  # cython.char



def test_carray_genexpr_pointer_char_7_12_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_char_7_12_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.char] = 'abc-def'

    return (item for item in carray[:7])  # cython.char



def test_carray_forin_constant_char_133_constant():
    """
    >>> charlist(test_carray_forin_constant_char_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.char[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.char
        items.append(item)
    return items



def test_carray_generator_constant_char_133_constant():
    """
    >>> charlist(list(test_carray_generator_constant_char_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.char[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.char
        yield item



def test_carray_listcomp_constant_char_133_constant():
    """
    >>> charlist(test_carray_listcomp_constant_char_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.char[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.char



def test_carray_setcomp_constant_char_133_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_char_133_constant()))
    [88]
    """
    carray: cython.char[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.char



def test_carray_genexpr_constant_char_133_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_char_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.char[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.char



def test_literal_forin_literal_char_133_literal():
    """
    >>> test_literal_forin_literal_char_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.char
        items.append(item)
    return items



def test_literal_generator_literal_char_133_literal():
    """
    >>> list(test_literal_generator_literal_char_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.char
        yield item



def test_literal_listcomp_literal_char_133_literal():
    """
    >>> test_literal_listcomp_literal_char_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.char



def test_literal_setcomp_literal_char_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_char_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.char



def test_literal_genexpr_literal_char_133_literal():
    """
    >>> list(test_literal_genexpr_literal_char_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.char



def test_carray_forin_pointer_char_133_pointer():
    """
    >>> charlist(test_carray_forin_pointer_char_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.char] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.char
        items.append(item)
    return items



def test_carray_generator_pointer_char_133_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_char_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.char] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.char
        yield item



def test_carray_listcomp_pointer_char_133_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_char_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.char] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.char



def test_carray_setcomp_pointer_char_133_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_char_133_pointer()))
    [88]
    """
    carray: cython.pointer[cython.char] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.char



def test_carray_genexpr_pointer_char_133_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_char_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.char] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.char



def test_carray_forin_constant_const_char_1_constant():
    """
    >>> test_carray_forin_constant_const_char_1_constant()
    [120]
    """
    carray: cython.const[cython.char][1] = b'x'

    items = []
    for item in carray:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_constant_const_char_1_constant():
    """
    >>> list(test_carray_generator_constant_const_char_1_constant())
    [120]
    """
    carray: cython.const[cython.char][1] = b'x'

    for item in carray:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_constant_const_char_1_constant():
    """
    >>> test_carray_listcomp_constant_const_char_1_constant()
    [120]
    """
    carray: cython.const[cython.char][1] = b'x'

    return [item for item in carray]  # cython.const[cython.char]



def test_carray_setcomp_constant_const_char_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_char_1_constant())
    [120]
    """
    carray: cython.const[cython.char][1] = b'x'

    return {item for item in carray}  # cython.const[cython.char]



def test_carray_genexpr_constant_const_char_1_constant():
    """
    >>> list(test_carray_genexpr_constant_const_char_1_constant())
    [120]
    """
    carray: cython.const[cython.char][1] = b'x'

    return (item for item in carray)  # cython.const[cython.char]



def test_literal_forin_literal_const_char_1_literal():
    """
    >>> test_literal_forin_literal_const_char_1_literal()
    [120]
    """


    items = []
    for item in b'x':  # cython.const[cython.char]
        items.append(item)
    return items



def test_literal_generator_literal_const_char_1_literal():
    """
    >>> list(test_literal_generator_literal_const_char_1_literal())
    [120]
    """


    for item in b'x':  # cython.const[cython.char]
        yield item



def test_literal_listcomp_literal_const_char_1_literal():
    """
    >>> test_literal_listcomp_literal_const_char_1_literal()
    [120]
    """


    return [item for item in b'x']  # cython.const[cython.char]



def test_literal_setcomp_literal_const_char_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_char_1_literal())
    [120]
    """


    return {item for item in b'x'}  # cython.const[cython.char]



def test_literal_genexpr_literal_const_char_1_literal():
    """
    >>> list(test_literal_genexpr_literal_const_char_1_literal())
    [120]
    """


    return (item for item in b'x')  # cython.const[cython.char]



def test_carray_forin_pointer_const_char_1_pointer():
    """
    >>> test_carray_forin_pointer_const_char_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'x'

    items = []
    for item in carray[:1]:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_pointer_const_char_1_pointer():
    """
    >>> list(test_carray_generator_pointer_const_char_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'x'

    for item in carray[:1]:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_pointer_const_char_1_pointer():
    """
    >>> test_carray_listcomp_pointer_const_char_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'x'

    return [item for item in carray[:1]]  # cython.const[cython.char]



def test_carray_setcomp_pointer_const_char_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_char_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'x'

    return {item for item in carray[:1]}  # cython.const[cython.char]



def test_carray_genexpr_pointer_const_char_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_char_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'x'

    return (item for item in carray[:1])  # cython.const[cython.char]



def test_carray_forin_constant_const_char_7_constant():
    """
    >>> test_carray_forin_constant_const_char_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.char][7] = b'abcdefg'

    items = []
    for item in carray:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_constant_const_char_7_constant():
    """
    >>> list(test_carray_generator_constant_const_char_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.char][7] = b'abcdefg'

    for item in carray:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_constant_const_char_7_constant():
    """
    >>> test_carray_listcomp_constant_const_char_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.char][7] = b'abcdefg'

    return [item for item in carray]  # cython.const[cython.char]



def test_carray_setcomp_constant_const_char_7_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_char_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.char][7] = b'abcdefg'

    return {item for item in carray}  # cython.const[cython.char]



def test_carray_genexpr_constant_const_char_7_constant():
    """
    >>> list(test_carray_genexpr_constant_const_char_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.char][7] = b'abcdefg'

    return (item for item in carray)  # cython.const[cython.char]



def test_literal_forin_literal_const_char_7_literal():
    """
    >>> test_literal_forin_literal_const_char_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    items = []
    for item in b'abcdefg':  # cython.const[cython.char]
        items.append(item)
    return items



def test_literal_generator_literal_const_char_7_literal():
    """
    >>> list(test_literal_generator_literal_const_char_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    for item in b'abcdefg':  # cython.const[cython.char]
        yield item



def test_literal_listcomp_literal_const_char_7_literal():
    """
    >>> test_literal_listcomp_literal_const_char_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    return [item for item in b'abcdefg']  # cython.const[cython.char]



def test_literal_setcomp_literal_const_char_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_char_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return {item for item in b'abcdefg'}  # cython.const[cython.char]



def test_literal_genexpr_literal_const_char_7_literal():
    """
    >>> list(test_literal_genexpr_literal_const_char_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return (item for item in b'abcdefg')  # cython.const[cython.char]



def test_carray_forin_pointer_const_char_7_pointer():
    """
    >>> test_carray_forin_pointer_const_char_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'abcdefg'

    items = []
    for item in carray[:7]:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_pointer_const_char_7_pointer():
    """
    >>> list(test_carray_generator_pointer_const_char_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'abcdefg'

    for item in carray[:7]:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_pointer_const_char_7_pointer():
    """
    >>> test_carray_listcomp_pointer_const_char_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'abcdefg'

    return [item for item in carray[:7]]  # cython.const[cython.char]



def test_carray_setcomp_pointer_const_char_7_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_char_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'abcdefg'

    return {item for item in carray[:7]}  # cython.const[cython.char]



def test_carray_genexpr_pointer_const_char_7_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_char_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'abcdefg'

    return (item for item in carray[:7])  # cython.const[cython.char]



def test_carray_forin_constant_const_char_100_constant():
    """
    >>> test_carray_forin_constant_const_char_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.char][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_constant_const_char_100_constant():
    """
    >>> list(test_carray_generator_constant_const_char_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.char][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_constant_const_char_100_constant():
    """
    >>> test_carray_listcomp_constant_const_char_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.char][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray]  # cython.const[cython.char]



def test_carray_setcomp_constant_const_char_100_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_char_100_constant())
    [120]
    """
    carray: cython.const[cython.char][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray}  # cython.const[cython.char]



def test_carray_genexpr_constant_const_char_100_constant():
    """
    >>> list(test_carray_genexpr_constant_const_char_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.char][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray)  # cython.const[cython.char]



def test_literal_forin_literal_const_char_100_literal():
    """
    >>> test_literal_forin_literal_const_char_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    items = []
    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.const[cython.char]
        items.append(item)
    return items



def test_literal_generator_literal_const_char_100_literal():
    """
    >>> list(test_literal_generator_literal_const_char_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.const[cython.char]
        yield item



def test_literal_listcomp_literal_const_char_100_literal():
    """
    >>> test_literal_listcomp_literal_const_char_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return [item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']  # cython.const[cython.char]



def test_literal_setcomp_literal_const_char_100_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_char_100_literal())
    [120]
    """


    return {item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}  # cython.const[cython.char]



def test_literal_genexpr_literal_const_char_100_literal():
    """
    >>> list(test_literal_genexpr_literal_const_char_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return (item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # cython.const[cython.char]



def test_carray_forin_pointer_const_char_100_pointer():
    """
    >>> test_carray_forin_pointer_const_char_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray[:100]:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_pointer_const_char_100_pointer():
    """
    >>> list(test_carray_generator_pointer_const_char_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray[:100]:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_pointer_const_char_100_pointer():
    """
    >>> test_carray_listcomp_pointer_const_char_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray[:100]]  # cython.const[cython.char]



def test_carray_setcomp_pointer_const_char_100_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_char_100_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray[:100]}  # cython.const[cython.char]



def test_carray_genexpr_pointer_const_char_100_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_char_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.char]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray[:100])  # cython.const[cython.char]



def test_carray_forin_constant_const_char_1_17_constant():
    """
    >>> charlist(test_carray_forin_constant_const_char_1_17_constant())
    [88]
    """
    carray: cython.const[cython.char][1] = 'X'

    items = []
    for item in carray:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_constant_const_char_1_17_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_char_1_17_constant()))
    [88]
    """
    carray: cython.const[cython.char][1] = 'X'

    for item in carray:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_constant_const_char_1_17_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_char_1_17_constant())
    [88]
    """
    carray: cython.const[cython.char][1] = 'X'

    return [item for item in carray]  # cython.const[cython.char]



def test_carray_setcomp_constant_const_char_1_17_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_char_1_17_constant()))
    [88]
    """
    carray: cython.const[cython.char][1] = 'X'

    return {item for item in carray}  # cython.const[cython.char]



def test_carray_genexpr_constant_const_char_1_17_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_char_1_17_constant()))
    [88]
    """
    carray: cython.const[cython.char][1] = 'X'

    return (item for item in carray)  # cython.const[cython.char]



def test_literal_forin_literal_const_char_1_17_literal():
    """
    >>> test_literal_forin_literal_const_char_1_17_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.const[cython.char]
        items.append(item)
    return items



def test_literal_generator_literal_const_char_1_17_literal():
    """
    >>> list(test_literal_generator_literal_const_char_1_17_literal())
    ['X']
    """


    for item in 'X':  # cython.const[cython.char]
        yield item



def test_literal_listcomp_literal_const_char_1_17_literal():
    """
    >>> test_literal_listcomp_literal_const_char_1_17_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.const[cython.char]



def test_literal_setcomp_literal_const_char_1_17_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_char_1_17_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.const[cython.char]



def test_literal_genexpr_literal_const_char_1_17_literal():
    """
    >>> list(test_literal_genexpr_literal_const_char_1_17_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.const[cython.char]



def test_carray_forin_pointer_const_char_1_17_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_char_1_17_pointer())
    [88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'X'

    items = []
    for item in carray[:1]:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_pointer_const_char_1_17_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_char_1_17_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'X'

    for item in carray[:1]:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_pointer_const_char_1_17_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_char_1_17_pointer())
    [88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'X'

    return [item for item in carray[:1]]  # cython.const[cython.char]



def test_carray_setcomp_pointer_const_char_1_17_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_char_1_17_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'X'

    return {item for item in carray[:1]}  # cython.const[cython.char]



def test_carray_genexpr_pointer_const_char_1_17_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_char_1_17_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'X'

    return (item for item in carray[:1])  # cython.const[cython.char]



def test_carray_forin_constant_const_char_7_18_constant():
    """
    >>> charlist(test_carray_forin_constant_const_char_7_18_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.char][7] = 'abc-def'

    items = []
    for item in carray:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_constant_const_char_7_18_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_char_7_18_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.char][7] = 'abc-def'

    for item in carray:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_constant_const_char_7_18_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_char_7_18_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.char][7] = 'abc-def'

    return [item for item in carray]  # cython.const[cython.char]



def test_carray_setcomp_constant_const_char_7_18_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_char_7_18_constant()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.const[cython.char][7] = 'abc-def'

    return {item for item in carray}  # cython.const[cython.char]



def test_carray_genexpr_constant_const_char_7_18_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_char_7_18_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.char][7] = 'abc-def'

    return (item for item in carray)  # cython.const[cython.char]



def test_literal_forin_literal_const_char_7_18_literal():
    """
    >>> test_literal_forin_literal_const_char_7_18_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.const[cython.char]
        items.append(item)
    return items



def test_literal_generator_literal_const_char_7_18_literal():
    """
    >>> list(test_literal_generator_literal_const_char_7_18_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.const[cython.char]
        yield item



def test_literal_listcomp_literal_const_char_7_18_literal():
    """
    >>> test_literal_listcomp_literal_const_char_7_18_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.const[cython.char]



def test_literal_setcomp_literal_const_char_7_18_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_char_7_18_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.const[cython.char]



def test_literal_genexpr_literal_const_char_7_18_literal():
    """
    >>> list(test_literal_genexpr_literal_const_char_7_18_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.const[cython.char]



def test_carray_forin_pointer_const_char_7_18_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_char_7_18_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_pointer_const_char_7_18_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_char_7_18_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'abc-def'

    for item in carray[:7]:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_pointer_const_char_7_18_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_char_7_18_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'abc-def'

    return [item for item in carray[:7]]  # cython.const[cython.char]



def test_carray_setcomp_pointer_const_char_7_18_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_char_7_18_pointer()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'abc-def'

    return {item for item in carray[:7]}  # cython.const[cython.char]



def test_carray_genexpr_pointer_const_char_7_18_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_char_7_18_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'abc-def'

    return (item for item in carray[:7])  # cython.const[cython.char]



def test_carray_forin_constant_const_char_133_constant():
    """
    >>> charlist(test_carray_forin_constant_const_char_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.char][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_constant_const_char_133_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_char_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.char][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_constant_const_char_133_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_char_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.char][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.const[cython.char]



def test_carray_setcomp_constant_const_char_133_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_char_133_constant()))
    [88]
    """
    carray: cython.const[cython.char][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.const[cython.char]



def test_carray_genexpr_constant_const_char_133_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_char_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.char][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.const[cython.char]



def test_literal_forin_literal_const_char_133_literal():
    """
    >>> test_literal_forin_literal_const_char_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.char]
        items.append(item)
    return items



def test_literal_generator_literal_const_char_133_literal():
    """
    >>> list(test_literal_generator_literal_const_char_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.char]
        yield item



def test_literal_listcomp_literal_const_char_133_literal():
    """
    >>> test_literal_listcomp_literal_const_char_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.const[cython.char]



def test_literal_setcomp_literal_const_char_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_char_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.const[cython.char]



def test_literal_genexpr_literal_const_char_133_literal():
    """
    >>> list(test_literal_genexpr_literal_const_char_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.const[cython.char]



def test_carray_forin_pointer_const_char_133_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_char_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.const[cython.char]
        items.append(item)
    return items



def test_carray_generator_pointer_const_char_133_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_char_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.const[cython.char]
        yield item



def test_carray_listcomp_pointer_const_char_133_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_char_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.const[cython.char]



def test_carray_setcomp_pointer_const_char_133_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_char_133_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.const[cython.char]



def test_carray_genexpr_pointer_const_char_133_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_char_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.char]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.const[cython.char]



def test_carray_forin_constant_uchar_1_constant():
    """
    >>> test_carray_forin_constant_uchar_1_constant()
    [120]
    """
    carray: cython.uchar[1] = b'x'

    items = []
    for item in carray:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_constant_uchar_1_constant():
    """
    >>> list(test_carray_generator_constant_uchar_1_constant())
    [120]
    """
    carray: cython.uchar[1] = b'x'

    for item in carray:  # cython.uchar
        yield item



def test_carray_listcomp_constant_uchar_1_constant():
    """
    >>> test_carray_listcomp_constant_uchar_1_constant()
    [120]
    """
    carray: cython.uchar[1] = b'x'

    return [item for item in carray]  # cython.uchar



def test_carray_setcomp_constant_uchar_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_uchar_1_constant())
    [120]
    """
    carray: cython.uchar[1] = b'x'

    return {item for item in carray}  # cython.uchar



def test_carray_genexpr_constant_uchar_1_constant():
    """
    >>> list(test_carray_genexpr_constant_uchar_1_constant())
    [120]
    """
    carray: cython.uchar[1] = b'x'

    return (item for item in carray)  # cython.uchar



def test_literal_forin_literal_uchar_1_literal():
    """
    >>> test_literal_forin_literal_uchar_1_literal()
    [120]
    """


    items = []
    for item in b'x':  # cython.uchar
        items.append(item)
    return items



def test_literal_generator_literal_uchar_1_literal():
    """
    >>> list(test_literal_generator_literal_uchar_1_literal())
    [120]
    """


    for item in b'x':  # cython.uchar
        yield item



def test_literal_listcomp_literal_uchar_1_literal():
    """
    >>> test_literal_listcomp_literal_uchar_1_literal()
    [120]
    """


    return [item for item in b'x']  # cython.uchar



def test_literal_setcomp_literal_uchar_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_uchar_1_literal())
    [120]
    """


    return {item for item in b'x'}  # cython.uchar



def test_literal_genexpr_literal_uchar_1_literal():
    """
    >>> list(test_literal_genexpr_literal_uchar_1_literal())
    [120]
    """


    return (item for item in b'x')  # cython.uchar



def test_carray_forin_pointer_uchar_1_pointer():
    """
    >>> test_carray_forin_pointer_uchar_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.uchar] = b'x'

    items = []
    for item in carray[:1]:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_pointer_uchar_1_pointer():
    """
    >>> list(test_carray_generator_pointer_uchar_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.uchar] = b'x'

    for item in carray[:1]:  # cython.uchar
        yield item



def test_carray_listcomp_pointer_uchar_1_pointer():
    """
    >>> test_carray_listcomp_pointer_uchar_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.uchar] = b'x'

    return [item for item in carray[:1]]  # cython.uchar



def test_carray_setcomp_pointer_uchar_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_uchar_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.uchar] = b'x'

    return {item for item in carray[:1]}  # cython.uchar



def test_carray_genexpr_pointer_uchar_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_uchar_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.uchar] = b'x'

    return (item for item in carray[:1])  # cython.uchar



def test_carray_forin_constant_uchar_7_constant():
    """
    >>> test_carray_forin_constant_uchar_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.uchar[7] = b'abcdefg'

    items = []
    for item in carray:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_constant_uchar_7_constant():
    """
    >>> list(test_carray_generator_constant_uchar_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.uchar[7] = b'abcdefg'

    for item in carray:  # cython.uchar
        yield item



def test_carray_listcomp_constant_uchar_7_constant():
    """
    >>> test_carray_listcomp_constant_uchar_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.uchar[7] = b'abcdefg'

    return [item for item in carray]  # cython.uchar



def test_carray_setcomp_constant_uchar_7_constant():
    """
    >>> sorted(test_carray_setcomp_constant_uchar_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.uchar[7] = b'abcdefg'

    return {item for item in carray}  # cython.uchar



def test_carray_genexpr_constant_uchar_7_constant():
    """
    >>> list(test_carray_genexpr_constant_uchar_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.uchar[7] = b'abcdefg'

    return (item for item in carray)  # cython.uchar



def test_literal_forin_literal_uchar_7_literal():
    """
    >>> test_literal_forin_literal_uchar_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    items = []
    for item in b'abcdefg':  # cython.uchar
        items.append(item)
    return items



def test_literal_generator_literal_uchar_7_literal():
    """
    >>> list(test_literal_generator_literal_uchar_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    for item in b'abcdefg':  # cython.uchar
        yield item



def test_literal_listcomp_literal_uchar_7_literal():
    """
    >>> test_literal_listcomp_literal_uchar_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    return [item for item in b'abcdefg']  # cython.uchar



def test_literal_setcomp_literal_uchar_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_uchar_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return {item for item in b'abcdefg'}  # cython.uchar



def test_literal_genexpr_literal_uchar_7_literal():
    """
    >>> list(test_literal_genexpr_literal_uchar_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return (item for item in b'abcdefg')  # cython.uchar



def test_carray_forin_pointer_uchar_7_pointer():
    """
    >>> test_carray_forin_pointer_uchar_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.uchar] = b'abcdefg'

    items = []
    for item in carray[:7]:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_pointer_uchar_7_pointer():
    """
    >>> list(test_carray_generator_pointer_uchar_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.uchar] = b'abcdefg'

    for item in carray[:7]:  # cython.uchar
        yield item



def test_carray_listcomp_pointer_uchar_7_pointer():
    """
    >>> test_carray_listcomp_pointer_uchar_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.uchar] = b'abcdefg'

    return [item for item in carray[:7]]  # cython.uchar



def test_carray_setcomp_pointer_uchar_7_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_uchar_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.uchar] = b'abcdefg'

    return {item for item in carray[:7]}  # cython.uchar



def test_carray_genexpr_pointer_uchar_7_pointer():
    """
    >>> list(test_carray_genexpr_pointer_uchar_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.uchar] = b'abcdefg'

    return (item for item in carray[:7])  # cython.uchar



def test_carray_forin_constant_uchar_100_constant():
    """
    >>> test_carray_forin_constant_uchar_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.uchar[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_constant_uchar_100_constant():
    """
    >>> list(test_carray_generator_constant_uchar_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.uchar[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray:  # cython.uchar
        yield item



def test_carray_listcomp_constant_uchar_100_constant():
    """
    >>> test_carray_listcomp_constant_uchar_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.uchar[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray]  # cython.uchar



def test_carray_setcomp_constant_uchar_100_constant():
    """
    >>> sorted(test_carray_setcomp_constant_uchar_100_constant())
    [120]
    """
    carray: cython.uchar[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray}  # cython.uchar



def test_carray_genexpr_constant_uchar_100_constant():
    """
    >>> list(test_carray_genexpr_constant_uchar_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.uchar[100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray)  # cython.uchar



def test_literal_forin_literal_uchar_100_literal():
    """
    >>> test_literal_forin_literal_uchar_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    items = []
    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.uchar
        items.append(item)
    return items



def test_literal_generator_literal_uchar_100_literal():
    """
    >>> list(test_literal_generator_literal_uchar_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.uchar
        yield item



def test_literal_listcomp_literal_uchar_100_literal():
    """
    >>> test_literal_listcomp_literal_uchar_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return [item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']  # cython.uchar



def test_literal_setcomp_literal_uchar_100_literal():
    """
    >>> sorted(test_literal_setcomp_literal_uchar_100_literal())
    [120]
    """


    return {item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}  # cython.uchar



def test_literal_genexpr_literal_uchar_100_literal():
    """
    >>> list(test_literal_genexpr_literal_uchar_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return (item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # cython.uchar



def test_carray_forin_pointer_uchar_100_pointer():
    """
    >>> test_carray_forin_pointer_uchar_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.uchar] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray[:100]:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_pointer_uchar_100_pointer():
    """
    >>> list(test_carray_generator_pointer_uchar_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.uchar] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray[:100]:  # cython.uchar
        yield item



def test_carray_listcomp_pointer_uchar_100_pointer():
    """
    >>> test_carray_listcomp_pointer_uchar_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.uchar] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray[:100]]  # cython.uchar



def test_carray_setcomp_pointer_uchar_100_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_uchar_100_pointer())
    [120]
    """
    carray: cython.pointer[cython.uchar] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray[:100]}  # cython.uchar



def test_carray_genexpr_pointer_uchar_100_pointer():
    """
    >>> list(test_carray_genexpr_pointer_uchar_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.uchar] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray[:100])  # cython.uchar



def test_carray_forin_constant_uchar_1_23_constant():
    """
    >>> charlist(test_carray_forin_constant_uchar_1_23_constant())
    [88]
    """
    carray: cython.uchar[1] = 'X'

    items = []
    for item in carray:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_constant_uchar_1_23_constant():
    """
    >>> charlist(list(test_carray_generator_constant_uchar_1_23_constant()))
    [88]
    """
    carray: cython.uchar[1] = 'X'

    for item in carray:  # cython.uchar
        yield item



def test_carray_listcomp_constant_uchar_1_23_constant():
    """
    >>> charlist(test_carray_listcomp_constant_uchar_1_23_constant())
    [88]
    """
    carray: cython.uchar[1] = 'X'

    return [item for item in carray]  # cython.uchar



def test_carray_setcomp_constant_uchar_1_23_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_uchar_1_23_constant()))
    [88]
    """
    carray: cython.uchar[1] = 'X'

    return {item for item in carray}  # cython.uchar



def test_carray_genexpr_constant_uchar_1_23_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_uchar_1_23_constant()))
    [88]
    """
    carray: cython.uchar[1] = 'X'

    return (item for item in carray)  # cython.uchar



def test_literal_forin_literal_uchar_1_23_literal():
    """
    >>> test_literal_forin_literal_uchar_1_23_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.uchar
        items.append(item)
    return items



def test_literal_generator_literal_uchar_1_23_literal():
    """
    >>> list(test_literal_generator_literal_uchar_1_23_literal())
    ['X']
    """


    for item in 'X':  # cython.uchar
        yield item



def test_literal_listcomp_literal_uchar_1_23_literal():
    """
    >>> test_literal_listcomp_literal_uchar_1_23_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.uchar



def test_literal_setcomp_literal_uchar_1_23_literal():
    """
    >>> sorted(test_literal_setcomp_literal_uchar_1_23_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.uchar



def test_literal_genexpr_literal_uchar_1_23_literal():
    """
    >>> list(test_literal_genexpr_literal_uchar_1_23_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.uchar



def test_carray_forin_pointer_uchar_1_23_pointer():
    """
    >>> charlist(test_carray_forin_pointer_uchar_1_23_pointer())
    [88]
    """
    carray: cython.pointer[cython.uchar] = 'X'

    items = []
    for item in carray[:1]:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_pointer_uchar_1_23_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_uchar_1_23_pointer()))
    [88]
    """
    carray: cython.pointer[cython.uchar] = 'X'

    for item in carray[:1]:  # cython.uchar
        yield item



def test_carray_listcomp_pointer_uchar_1_23_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_uchar_1_23_pointer())
    [88]
    """
    carray: cython.pointer[cython.uchar] = 'X'

    return [item for item in carray[:1]]  # cython.uchar



def test_carray_setcomp_pointer_uchar_1_23_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_uchar_1_23_pointer()))
    [88]
    """
    carray: cython.pointer[cython.uchar] = 'X'

    return {item for item in carray[:1]}  # cython.uchar



def test_carray_genexpr_pointer_uchar_1_23_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_uchar_1_23_pointer()))
    [88]
    """
    carray: cython.pointer[cython.uchar] = 'X'

    return (item for item in carray[:1])  # cython.uchar



def test_carray_forin_constant_uchar_7_24_constant():
    """
    >>> charlist(test_carray_forin_constant_uchar_7_24_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.uchar[7] = 'abc-def'

    items = []
    for item in carray:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_constant_uchar_7_24_constant():
    """
    >>> charlist(list(test_carray_generator_constant_uchar_7_24_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.uchar[7] = 'abc-def'

    for item in carray:  # cython.uchar
        yield item



def test_carray_listcomp_constant_uchar_7_24_constant():
    """
    >>> charlist(test_carray_listcomp_constant_uchar_7_24_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.uchar[7] = 'abc-def'

    return [item for item in carray]  # cython.uchar



def test_carray_setcomp_constant_uchar_7_24_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_uchar_7_24_constant()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.uchar[7] = 'abc-def'

    return {item for item in carray}  # cython.uchar



def test_carray_genexpr_constant_uchar_7_24_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_uchar_7_24_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.uchar[7] = 'abc-def'

    return (item for item in carray)  # cython.uchar



def test_literal_forin_literal_uchar_7_24_literal():
    """
    >>> test_literal_forin_literal_uchar_7_24_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.uchar
        items.append(item)
    return items



def test_literal_generator_literal_uchar_7_24_literal():
    """
    >>> list(test_literal_generator_literal_uchar_7_24_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.uchar
        yield item



def test_literal_listcomp_literal_uchar_7_24_literal():
    """
    >>> test_literal_listcomp_literal_uchar_7_24_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.uchar



def test_literal_setcomp_literal_uchar_7_24_literal():
    """
    >>> sorted(test_literal_setcomp_literal_uchar_7_24_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.uchar



def test_literal_genexpr_literal_uchar_7_24_literal():
    """
    >>> list(test_literal_genexpr_literal_uchar_7_24_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.uchar



def test_carray_forin_pointer_uchar_7_24_pointer():
    """
    >>> charlist(test_carray_forin_pointer_uchar_7_24_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.uchar] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_pointer_uchar_7_24_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_uchar_7_24_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.uchar] = 'abc-def'

    for item in carray[:7]:  # cython.uchar
        yield item



def test_carray_listcomp_pointer_uchar_7_24_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_uchar_7_24_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.uchar] = 'abc-def'

    return [item for item in carray[:7]]  # cython.uchar



def test_carray_setcomp_pointer_uchar_7_24_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_uchar_7_24_pointer()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.pointer[cython.uchar] = 'abc-def'

    return {item for item in carray[:7]}  # cython.uchar



def test_carray_genexpr_pointer_uchar_7_24_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_uchar_7_24_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.uchar] = 'abc-def'

    return (item for item in carray[:7])  # cython.uchar



def test_carray_forin_constant_uchar_133_constant():
    """
    >>> charlist(test_carray_forin_constant_uchar_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.uchar[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_constant_uchar_133_constant():
    """
    >>> charlist(list(test_carray_generator_constant_uchar_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.uchar[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.uchar
        yield item



def test_carray_listcomp_constant_uchar_133_constant():
    """
    >>> charlist(test_carray_listcomp_constant_uchar_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.uchar[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.uchar



def test_carray_setcomp_constant_uchar_133_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_uchar_133_constant()))
    [88]
    """
    carray: cython.uchar[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.uchar



def test_carray_genexpr_constant_uchar_133_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_uchar_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.uchar[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.uchar



def test_literal_forin_literal_uchar_133_literal():
    """
    >>> test_literal_forin_literal_uchar_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.uchar
        items.append(item)
    return items



def test_literal_generator_literal_uchar_133_literal():
    """
    >>> list(test_literal_generator_literal_uchar_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.uchar
        yield item



def test_literal_listcomp_literal_uchar_133_literal():
    """
    >>> test_literal_listcomp_literal_uchar_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.uchar



def test_literal_setcomp_literal_uchar_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_uchar_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.uchar



def test_literal_genexpr_literal_uchar_133_literal():
    """
    >>> list(test_literal_genexpr_literal_uchar_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.uchar



def test_carray_forin_pointer_uchar_133_pointer():
    """
    >>> charlist(test_carray_forin_pointer_uchar_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.uchar] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.uchar
        items.append(item)
    return items



def test_carray_generator_pointer_uchar_133_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_uchar_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.uchar] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.uchar
        yield item



def test_carray_listcomp_pointer_uchar_133_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_uchar_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.uchar] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.uchar



def test_carray_setcomp_pointer_uchar_133_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_uchar_133_pointer()))
    [88]
    """
    carray: cython.pointer[cython.uchar] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.uchar



def test_carray_genexpr_pointer_uchar_133_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_uchar_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.uchar] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.uchar



def test_carray_forin_constant_const_uchar_1_constant():
    """
    >>> test_carray_forin_constant_const_uchar_1_constant()
    [120]
    """
    carray: cython.const[cython.uchar][1] = b'x'

    items = []
    for item in carray:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_constant_const_uchar_1_constant():
    """
    >>> list(test_carray_generator_constant_const_uchar_1_constant())
    [120]
    """
    carray: cython.const[cython.uchar][1] = b'x'

    for item in carray:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_constant_const_uchar_1_constant():
    """
    >>> test_carray_listcomp_constant_const_uchar_1_constant()
    [120]
    """
    carray: cython.const[cython.uchar][1] = b'x'

    return [item for item in carray]  # cython.const[cython.uchar]



def test_carray_setcomp_constant_const_uchar_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_uchar_1_constant())
    [120]
    """
    carray: cython.const[cython.uchar][1] = b'x'

    return {item for item in carray}  # cython.const[cython.uchar]



def test_carray_genexpr_constant_const_uchar_1_constant():
    """
    >>> list(test_carray_genexpr_constant_const_uchar_1_constant())
    [120]
    """
    carray: cython.const[cython.uchar][1] = b'x'

    return (item for item in carray)  # cython.const[cython.uchar]



def test_literal_forin_literal_const_uchar_1_literal():
    """
    >>> test_literal_forin_literal_const_uchar_1_literal()
    [120]
    """


    items = []
    for item in b'x':  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_literal_generator_literal_const_uchar_1_literal():
    """
    >>> list(test_literal_generator_literal_const_uchar_1_literal())
    [120]
    """


    for item in b'x':  # cython.const[cython.uchar]
        yield item



def test_literal_listcomp_literal_const_uchar_1_literal():
    """
    >>> test_literal_listcomp_literal_const_uchar_1_literal()
    [120]
    """


    return [item for item in b'x']  # cython.const[cython.uchar]



def test_literal_setcomp_literal_const_uchar_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_uchar_1_literal())
    [120]
    """


    return {item for item in b'x'}  # cython.const[cython.uchar]



def test_literal_genexpr_literal_const_uchar_1_literal():
    """
    >>> list(test_literal_genexpr_literal_const_uchar_1_literal())
    [120]
    """


    return (item for item in b'x')  # cython.const[cython.uchar]



def test_carray_forin_pointer_const_uchar_1_pointer():
    """
    >>> test_carray_forin_pointer_const_uchar_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'x'

    items = []
    for item in carray[:1]:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_pointer_const_uchar_1_pointer():
    """
    >>> list(test_carray_generator_pointer_const_uchar_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'x'

    for item in carray[:1]:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_pointer_const_uchar_1_pointer():
    """
    >>> test_carray_listcomp_pointer_const_uchar_1_pointer()
    [120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'x'

    return [item for item in carray[:1]]  # cython.const[cython.uchar]



def test_carray_setcomp_pointer_const_uchar_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_uchar_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'x'

    return {item for item in carray[:1]}  # cython.const[cython.uchar]



def test_carray_genexpr_pointer_const_uchar_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_uchar_1_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'x'

    return (item for item in carray[:1])  # cython.const[cython.uchar]



def test_carray_forin_constant_const_uchar_7_constant():
    """
    >>> test_carray_forin_constant_const_uchar_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.uchar][7] = b'abcdefg'

    items = []
    for item in carray:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_constant_const_uchar_7_constant():
    """
    >>> list(test_carray_generator_constant_const_uchar_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.uchar][7] = b'abcdefg'

    for item in carray:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_constant_const_uchar_7_constant():
    """
    >>> test_carray_listcomp_constant_const_uchar_7_constant()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.uchar][7] = b'abcdefg'

    return [item for item in carray]  # cython.const[cython.uchar]



def test_carray_setcomp_constant_const_uchar_7_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_uchar_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.uchar][7] = b'abcdefg'

    return {item for item in carray}  # cython.const[cython.uchar]



def test_carray_genexpr_constant_const_uchar_7_constant():
    """
    >>> list(test_carray_genexpr_constant_const_uchar_7_constant())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.const[cython.uchar][7] = b'abcdefg'

    return (item for item in carray)  # cython.const[cython.uchar]



def test_literal_forin_literal_const_uchar_7_literal():
    """
    >>> test_literal_forin_literal_const_uchar_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    items = []
    for item in b'abcdefg':  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_literal_generator_literal_const_uchar_7_literal():
    """
    >>> list(test_literal_generator_literal_const_uchar_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    for item in b'abcdefg':  # cython.const[cython.uchar]
        yield item



def test_literal_listcomp_literal_const_uchar_7_literal():
    """
    >>> test_literal_listcomp_literal_const_uchar_7_literal()
    [97, 98, 99, 100, 101, 102, 103]
    """


    return [item for item in b'abcdefg']  # cython.const[cython.uchar]



def test_literal_setcomp_literal_const_uchar_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_uchar_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return {item for item in b'abcdefg'}  # cython.const[cython.uchar]



def test_literal_genexpr_literal_const_uchar_7_literal():
    """
    >>> list(test_literal_genexpr_literal_const_uchar_7_literal())
    [97, 98, 99, 100, 101, 102, 103]
    """


    return (item for item in b'abcdefg')  # cython.const[cython.uchar]



def test_carray_forin_pointer_const_uchar_7_pointer():
    """
    >>> test_carray_forin_pointer_const_uchar_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'abcdefg'

    items = []
    for item in carray[:7]:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_pointer_const_uchar_7_pointer():
    """
    >>> list(test_carray_generator_pointer_const_uchar_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'abcdefg'

    for item in carray[:7]:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_pointer_const_uchar_7_pointer():
    """
    >>> test_carray_listcomp_pointer_const_uchar_7_pointer()
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'abcdefg'

    return [item for item in carray[:7]]  # cython.const[cython.uchar]



def test_carray_setcomp_pointer_const_uchar_7_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_uchar_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'abcdefg'

    return {item for item in carray[:7]}  # cython.const[cython.uchar]



def test_carray_genexpr_pointer_const_uchar_7_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_uchar_7_pointer())
    [97, 98, 99, 100, 101, 102, 103]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'abcdefg'

    return (item for item in carray[:7])  # cython.const[cython.uchar]



def test_carray_forin_constant_const_uchar_100_constant():
    """
    >>> test_carray_forin_constant_const_uchar_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.uchar][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_constant_const_uchar_100_constant():
    """
    >>> list(test_carray_generator_constant_const_uchar_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.uchar][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_constant_const_uchar_100_constant():
    """
    >>> test_carray_listcomp_constant_const_uchar_100_constant()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.uchar][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray]  # cython.const[cython.uchar]



def test_carray_setcomp_constant_const_uchar_100_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_uchar_100_constant())
    [120]
    """
    carray: cython.const[cython.uchar][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray}  # cython.const[cython.uchar]



def test_carray_genexpr_constant_const_uchar_100_constant():
    """
    >>> list(test_carray_genexpr_constant_const_uchar_100_constant())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.const[cython.uchar][100] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray)  # cython.const[cython.uchar]



def test_literal_forin_literal_const_uchar_100_literal():
    """
    >>> test_literal_forin_literal_const_uchar_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    items = []
    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_literal_generator_literal_const_uchar_100_literal():
    """
    >>> list(test_literal_generator_literal_const_uchar_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':  # cython.const[cython.uchar]
        yield item



def test_literal_listcomp_literal_const_uchar_100_literal():
    """
    >>> test_literal_listcomp_literal_const_uchar_100_literal()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return [item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']  # cython.const[cython.uchar]



def test_literal_setcomp_literal_const_uchar_100_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_uchar_100_literal())
    [120]
    """


    return {item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}  # cython.const[cython.uchar]



def test_literal_genexpr_literal_const_uchar_100_literal():
    """
    >>> list(test_literal_genexpr_literal_const_uchar_100_literal())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """


    return (item for item in b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # cython.const[cython.uchar]



def test_carray_forin_pointer_const_uchar_100_pointer():
    """
    >>> test_carray_forin_pointer_const_uchar_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    items = []
    for item in carray[:100]:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_pointer_const_uchar_100_pointer():
    """
    >>> list(test_carray_generator_pointer_const_uchar_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    for item in carray[:100]:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_pointer_const_uchar_100_pointer():
    """
    >>> test_carray_listcomp_pointer_const_uchar_100_pointer()
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return [item for item in carray[:100]]  # cython.const[cython.uchar]



def test_carray_setcomp_pointer_const_uchar_100_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_uchar_100_pointer())
    [120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return {item for item in carray[:100]}  # cython.const[cython.uchar]



def test_carray_genexpr_pointer_const_uchar_100_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_uchar_100_pointer())
    [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    return (item for item in carray[:100])  # cython.const[cython.uchar]



def test_carray_forin_constant_const_uchar_1_29_constant():
    """
    >>> charlist(test_carray_forin_constant_const_uchar_1_29_constant())
    [88]
    """
    carray: cython.const[cython.uchar][1] = 'X'

    items = []
    for item in carray:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_constant_const_uchar_1_29_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_uchar_1_29_constant()))
    [88]
    """
    carray: cython.const[cython.uchar][1] = 'X'

    for item in carray:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_constant_const_uchar_1_29_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_uchar_1_29_constant())
    [88]
    """
    carray: cython.const[cython.uchar][1] = 'X'

    return [item for item in carray]  # cython.const[cython.uchar]



def test_carray_setcomp_constant_const_uchar_1_29_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_uchar_1_29_constant()))
    [88]
    """
    carray: cython.const[cython.uchar][1] = 'X'

    return {item for item in carray}  # cython.const[cython.uchar]



def test_carray_genexpr_constant_const_uchar_1_29_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_uchar_1_29_constant()))
    [88]
    """
    carray: cython.const[cython.uchar][1] = 'X'

    return (item for item in carray)  # cython.const[cython.uchar]



def test_literal_forin_literal_const_uchar_1_29_literal():
    """
    >>> test_literal_forin_literal_const_uchar_1_29_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_literal_generator_literal_const_uchar_1_29_literal():
    """
    >>> list(test_literal_generator_literal_const_uchar_1_29_literal())
    ['X']
    """


    for item in 'X':  # cython.const[cython.uchar]
        yield item



def test_literal_listcomp_literal_const_uchar_1_29_literal():
    """
    >>> test_literal_listcomp_literal_const_uchar_1_29_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.const[cython.uchar]



def test_literal_setcomp_literal_const_uchar_1_29_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_uchar_1_29_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.const[cython.uchar]



def test_literal_genexpr_literal_const_uchar_1_29_literal():
    """
    >>> list(test_literal_genexpr_literal_const_uchar_1_29_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.const[cython.uchar]



def test_carray_forin_pointer_const_uchar_1_29_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_uchar_1_29_pointer())
    [88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'X'

    items = []
    for item in carray[:1]:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_pointer_const_uchar_1_29_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_uchar_1_29_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'X'

    for item in carray[:1]:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_pointer_const_uchar_1_29_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_uchar_1_29_pointer())
    [88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'X'

    return [item for item in carray[:1]]  # cython.const[cython.uchar]



def test_carray_setcomp_pointer_const_uchar_1_29_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_uchar_1_29_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'X'

    return {item for item in carray[:1]}  # cython.const[cython.uchar]



def test_carray_genexpr_pointer_const_uchar_1_29_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_uchar_1_29_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'X'

    return (item for item in carray[:1])  # cython.const[cython.uchar]



def test_carray_forin_constant_const_uchar_7_30_constant():
    """
    >>> charlist(test_carray_forin_constant_const_uchar_7_30_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.uchar][7] = 'abc-def'

    items = []
    for item in carray:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_constant_const_uchar_7_30_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_uchar_7_30_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.uchar][7] = 'abc-def'

    for item in carray:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_constant_const_uchar_7_30_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_uchar_7_30_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.uchar][7] = 'abc-def'

    return [item for item in carray]  # cython.const[cython.uchar]



def test_carray_setcomp_constant_const_uchar_7_30_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_uchar_7_30_constant()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.const[cython.uchar][7] = 'abc-def'

    return {item for item in carray}  # cython.const[cython.uchar]



def test_carray_genexpr_constant_const_uchar_7_30_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_uchar_7_30_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.uchar][7] = 'abc-def'

    return (item for item in carray)  # cython.const[cython.uchar]



def test_literal_forin_literal_const_uchar_7_30_literal():
    """
    >>> test_literal_forin_literal_const_uchar_7_30_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_literal_generator_literal_const_uchar_7_30_literal():
    """
    >>> list(test_literal_generator_literal_const_uchar_7_30_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.const[cython.uchar]
        yield item



def test_literal_listcomp_literal_const_uchar_7_30_literal():
    """
    >>> test_literal_listcomp_literal_const_uchar_7_30_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.const[cython.uchar]



def test_literal_setcomp_literal_const_uchar_7_30_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_uchar_7_30_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.const[cython.uchar]



def test_literal_genexpr_literal_const_uchar_7_30_literal():
    """
    >>> list(test_literal_genexpr_literal_const_uchar_7_30_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.const[cython.uchar]



def test_carray_forin_pointer_const_uchar_7_30_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_uchar_7_30_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_pointer_const_uchar_7_30_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_uchar_7_30_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'abc-def'

    for item in carray[:7]:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_pointer_const_uchar_7_30_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_uchar_7_30_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'abc-def'

    return [item for item in carray[:7]]  # cython.const[cython.uchar]



def test_carray_setcomp_pointer_const_uchar_7_30_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_uchar_7_30_pointer()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'abc-def'

    return {item for item in carray[:7]}  # cython.const[cython.uchar]



def test_carray_genexpr_pointer_const_uchar_7_30_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_uchar_7_30_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'abc-def'

    return (item for item in carray[:7])  # cython.const[cython.uchar]



def test_carray_forin_constant_const_uchar_133_constant():
    """
    >>> charlist(test_carray_forin_constant_const_uchar_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.uchar][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_constant_const_uchar_133_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_uchar_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.uchar][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_constant_const_uchar_133_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_uchar_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.uchar][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.const[cython.uchar]



def test_carray_setcomp_constant_const_uchar_133_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_uchar_133_constant()))
    [88]
    """
    carray: cython.const[cython.uchar][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.const[cython.uchar]



def test_carray_genexpr_constant_const_uchar_133_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_uchar_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.uchar][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.const[cython.uchar]



def test_literal_forin_literal_const_uchar_133_literal():
    """
    >>> test_literal_forin_literal_const_uchar_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_literal_generator_literal_const_uchar_133_literal():
    """
    >>> list(test_literal_generator_literal_const_uchar_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.uchar]
        yield item



def test_literal_listcomp_literal_const_uchar_133_literal():
    """
    >>> test_literal_listcomp_literal_const_uchar_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.const[cython.uchar]



def test_literal_setcomp_literal_const_uchar_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_uchar_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.const[cython.uchar]



def test_literal_genexpr_literal_const_uchar_133_literal():
    """
    >>> list(test_literal_genexpr_literal_const_uchar_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.const[cython.uchar]



def test_carray_forin_pointer_const_uchar_133_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_uchar_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.const[cython.uchar]
        items.append(item)
    return items



def test_carray_generator_pointer_const_uchar_133_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_uchar_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.const[cython.uchar]
        yield item



def test_carray_listcomp_pointer_const_uchar_133_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_uchar_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.const[cython.uchar]



def test_carray_setcomp_pointer_const_uchar_133_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_uchar_133_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.const[cython.uchar]



def test_carray_genexpr_pointer_const_uchar_133_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_uchar_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.uchar]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.const[cython.uchar]



def test_carray_forin_constant_Py_UCS4_1_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_1_constant()
    ['X']
    """
    carray: cython.Py_UCS4[1] = 'X'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_1_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_1_constant())
    ['X']
    """
    carray: cython.Py_UCS4[1] = 'X'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_1_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_1_constant()
    ['X']
    """
    carray: cython.Py_UCS4[1] = 'X'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_1_constant())
    ['X']
    """
    carray: cython.Py_UCS4[1] = 'X'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_1_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_1_constant())
    ['X']
    """
    carray: cython.Py_UCS4[1] = 'X'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_1_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_1_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_1_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_1_literal())
    ['X']
    """


    for item in 'X':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_1_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_1_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_1_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_1_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_1_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_1_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_1_pointer()
    ['X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'X'

    items = []
    for item in carray[:1]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_1_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_1_pointer())
    ['X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'X'

    for item in carray[:1]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_1_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_1_pointer()
    ['X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'X'

    return [item for item in carray[:1]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_1_pointer())
    ['X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'X'

    return {item for item in carray[:1]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_1_pointer())
    ['X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'X'

    return (item for item in carray[:1])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_7_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_7_constant()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.Py_UCS4[7] = 'abc-def'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_7_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_7_constant())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.Py_UCS4[7] = 'abc-def'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_7_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_7_constant()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.Py_UCS4[7] = 'abc-def'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_7_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_7_constant())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """
    carray: cython.Py_UCS4[7] = 'abc-def'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_7_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_7_constant())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.Py_UCS4[7] = 'abc-def'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_7_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_7_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_7_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_7_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_7_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_7_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_7_pointer()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_7_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_7_pointer())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'abc-def'

    for item in carray[:7]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_7_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_7_pointer()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'abc-def'

    return [item for item in carray[:7]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_7_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_7_pointer())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'abc-def'

    return {item for item in carray[:7]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_7_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_7_pointer())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'abc-def'

    return (item for item in carray[:7])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_133_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_133_constant()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.Py_UCS4[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_133_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_133_constant())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.Py_UCS4[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_133_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_133_constant()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.Py_UCS4[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_133_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_133_constant())
    ['X']
    """
    carray: cython.Py_UCS4[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_133_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_133_constant())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.Py_UCS4[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_133_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_133_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_133_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_133_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_133_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_133_pointer()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_133_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_133_pointer())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_133_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_133_pointer()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_133_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_133_pointer())
    ['X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_133_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_133_pointer())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.Py_UCS4] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_1_35_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_1_35_constant()
    ['☃']
    """
    carray: cython.Py_UCS4[1] = '☃'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_1_35_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_1_35_constant())
    ['☃']
    """
    carray: cython.Py_UCS4[1] = '☃'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_1_35_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_1_35_constant()
    ['☃']
    """
    carray: cython.Py_UCS4[1] = '☃'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_1_35_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_1_35_constant())
    ['☃']
    """
    carray: cython.Py_UCS4[1] = '☃'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_1_35_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_1_35_constant())
    ['☃']
    """
    carray: cython.Py_UCS4[1] = '☃'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_1_35_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_1_35_literal()
    ['☃']
    """


    items = []
    for item in '☃':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_1_35_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_1_35_literal())
    ['☃']
    """


    for item in '☃':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_1_35_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_1_35_literal()
    ['☃']
    """


    return [item for item in '☃']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_1_35_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_1_35_literal())
    ['☃']
    """


    return {item for item in '☃'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_1_35_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_1_35_literal())
    ['☃']
    """


    return (item for item in '☃')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_1_35_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_1_35_pointer()
    ['☃']
    """
    carray: cython.pointer[cython.Py_UCS4] = '☃'

    items = []
    for item in carray[:1]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_1_35_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_1_35_pointer())
    ['☃']
    """
    carray: cython.pointer[cython.Py_UCS4] = '☃'

    for item in carray[:1]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_1_35_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_1_35_pointer()
    ['☃']
    """
    carray: cython.pointer[cython.Py_UCS4] = '☃'

    return [item for item in carray[:1]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_1_35_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_1_35_pointer())
    ['☃']
    """
    carray: cython.pointer[cython.Py_UCS4] = '☃'

    return {item for item in carray[:1]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_1_35_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_1_35_pointer())
    ['☃']
    """
    carray: cython.pointer[cython.Py_UCS4] = '☃'

    return (item for item in carray[:1])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_11_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_11_constant()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.Py_UCS4[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_11_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_11_constant())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.Py_UCS4[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_11_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_11_constant()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.Py_UCS4[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_11_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_11_constant())
    ['∑']
    """
    carray: cython.Py_UCS4[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_11_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_11_constant())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.Py_UCS4[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_11_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    items = []
    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_11_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_11_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return [item for item in '∑∑∑∑∑∑∑∑∑∑∑']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_11_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_11_literal())
    ['∑']
    """


    return {item for item in '∑∑∑∑∑∑∑∑∑∑∑'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_11_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return (item for item in '∑∑∑∑∑∑∑∑∑∑∑')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_11_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_11_pointer()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray[:11]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_11_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_11_pointer())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray[:11]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_11_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_11_pointer()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray[:11]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_11_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_11_pointer())
    ['∑']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray[:11]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_11_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_11_pointer())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray[:11])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_21_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_21_constant()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.Py_UCS4[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_21_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_21_constant())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.Py_UCS4[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_21_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_21_constant()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.Py_UCS4[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_21_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_21_constant())
    [' ', 'ℇ', '∑']
    """
    carray: cython.Py_UCS4[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_21_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_21_constant())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.Py_UCS4[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_21_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    items = []
    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_21_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_21_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return [item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_21_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_21_literal())
    [' ', 'ℇ', '∑']
    """


    return {item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_21_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return (item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_21_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_21_pointer()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray[:21]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_21_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_21_pointer())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray[:21]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_21_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_21_pointer()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray[:21]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_21_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_21_pointer())
    [' ', 'ℇ', '∑']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray[:21]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_21_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_21_pointer())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.Py_UCS4] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray[:21])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_2_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_2_constant()
    ['😇', '😌']
    """
    carray: cython.Py_UCS4[2] = '😇😌'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_2_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_2_constant())
    ['😇', '😌']
    """
    carray: cython.Py_UCS4[2] = '😇😌'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_2_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_2_constant()
    ['😇', '😌']
    """
    carray: cython.Py_UCS4[2] = '😇😌'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_2_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_2_constant())
    ['😇', '😌']
    """
    carray: cython.Py_UCS4[2] = '😇😌'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_2_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_2_constant())
    ['😇', '😌']
    """
    carray: cython.Py_UCS4[2] = '😇😌'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_2_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_2_literal()
    ['😇', '😌']
    """


    items = []
    for item in '😇😌':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_2_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_2_literal())
    ['😇', '😌']
    """


    for item in '😇😌':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_2_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_2_literal()
    ['😇', '😌']
    """


    return [item for item in '😇😌']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_2_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_2_literal())
    ['😇', '😌']
    """


    return {item for item in '😇😌'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_2_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_2_literal())
    ['😇', '😌']
    """


    return (item for item in '😇😌')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_2_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_2_pointer()
    ['😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌'

    items = []
    for item in carray[:2]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_2_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_2_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌'

    for item in carray[:2]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_2_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_2_pointer()
    ['😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌'

    return [item for item in carray[:2]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_2_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_2_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌'

    return {item for item in carray[:2]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_2_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_2_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌'

    return (item for item in carray[:2])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_3_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_3_constant()
    ['😇', 'x', '😌']
    """
    carray: cython.Py_UCS4[3] = '😇x😌'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_3_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_3_constant())
    ['😇', 'x', '😌']
    """
    carray: cython.Py_UCS4[3] = '😇x😌'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_3_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_3_constant()
    ['😇', 'x', '😌']
    """
    carray: cython.Py_UCS4[3] = '😇x😌'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_3_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_3_constant())
    ['x', '😇', '😌']
    """
    carray: cython.Py_UCS4[3] = '😇x😌'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_3_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_3_constant())
    ['😇', 'x', '😌']
    """
    carray: cython.Py_UCS4[3] = '😇x😌'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_3_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_3_literal()
    ['😇', 'x', '😌']
    """


    items = []
    for item in '😇x😌':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_3_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_3_literal())
    ['😇', 'x', '😌']
    """


    for item in '😇x😌':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_3_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_3_literal()
    ['😇', 'x', '😌']
    """


    return [item for item in '😇x😌']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_3_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_3_literal())
    ['x', '😇', '😌']
    """


    return {item for item in '😇x😌'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_3_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_3_literal())
    ['😇', 'x', '😌']
    """


    return (item for item in '😇x😌')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_3_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_3_pointer()
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇x😌'

    items = []
    for item in carray[:3]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_3_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_3_pointer())
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇x😌'

    for item in carray[:3]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_3_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_3_pointer()
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇x😌'

    return [item for item in carray[:3]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_3_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_3_pointer())
    ['x', '😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇x😌'

    return {item for item in carray[:3]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_3_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_3_pointer())
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇x😌'

    return (item for item in carray[:3])  # cython.Py_UCS4



def test_carray_forin_constant_Py_UCS4_14_constant():
    """
    >>> test_carray_forin_constant_Py_UCS4_14_constant()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.Py_UCS4[14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    items = []
    for item in carray:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_constant_Py_UCS4_14_constant():
    """
    >>> list(test_carray_generator_constant_Py_UCS4_14_constant())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.Py_UCS4[14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    for item in carray:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_constant_Py_UCS4_14_constant():
    """
    >>> test_carray_listcomp_constant_Py_UCS4_14_constant()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.Py_UCS4[14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return [item for item in carray]  # cython.Py_UCS4



def test_carray_setcomp_constant_Py_UCS4_14_constant():
    """
    >>> sorted(test_carray_setcomp_constant_Py_UCS4_14_constant())
    ['😇', '😌']
    """
    carray: cython.Py_UCS4[14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return {item for item in carray}  # cython.Py_UCS4



def test_carray_genexpr_constant_Py_UCS4_14_constant():
    """
    >>> list(test_carray_genexpr_constant_Py_UCS4_14_constant())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.Py_UCS4[14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return (item for item in carray)  # cython.Py_UCS4



def test_literal_forin_literal_Py_UCS4_14_literal():
    """
    >>> test_literal_forin_literal_Py_UCS4_14_literal()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    items = []
    for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌':  # cython.Py_UCS4
        items.append(item)
    return items



def test_literal_generator_literal_Py_UCS4_14_literal():
    """
    >>> list(test_literal_generator_literal_Py_UCS4_14_literal())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌':  # cython.Py_UCS4
        yield item



def test_literal_listcomp_literal_Py_UCS4_14_literal():
    """
    >>> test_literal_listcomp_literal_Py_UCS4_14_literal()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    return [item for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌']  # cython.Py_UCS4



def test_literal_setcomp_literal_Py_UCS4_14_literal():
    """
    >>> sorted(test_literal_setcomp_literal_Py_UCS4_14_literal())
    ['😇', '😌']
    """


    return {item for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'}  # cython.Py_UCS4



def test_literal_genexpr_literal_Py_UCS4_14_literal():
    """
    >>> list(test_literal_genexpr_literal_Py_UCS4_14_literal())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    return (item for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌')  # cython.Py_UCS4



def test_carray_forin_pointer_Py_UCS4_14_pointer():
    """
    >>> test_carray_forin_pointer_Py_UCS4_14_pointer()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    items = []
    for item in carray[:14]:  # cython.Py_UCS4
        items.append(item)
    return items



def test_carray_generator_pointer_Py_UCS4_14_pointer():
    """
    >>> list(test_carray_generator_pointer_Py_UCS4_14_pointer())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    for item in carray[:14]:  # cython.Py_UCS4
        yield item



def test_carray_listcomp_pointer_Py_UCS4_14_pointer():
    """
    >>> test_carray_listcomp_pointer_Py_UCS4_14_pointer()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return [item for item in carray[:14]]  # cython.Py_UCS4



def test_carray_setcomp_pointer_Py_UCS4_14_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_Py_UCS4_14_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return {item for item in carray[:14]}  # cython.Py_UCS4



def test_carray_genexpr_pointer_Py_UCS4_14_pointer():
    """
    >>> list(test_carray_genexpr_pointer_Py_UCS4_14_pointer())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.Py_UCS4] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return (item for item in carray[:14])  # cython.Py_UCS4



def test_carray_forin_constant_const_Py_UCS4_1_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_1_constant()
    ['X']
    """
    carray: cython.const[cython.Py_UCS4][1] = 'X'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_1_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_1_constant())
    ['X']
    """
    carray: cython.const[cython.Py_UCS4][1] = 'X'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_1_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_1_constant()
    ['X']
    """
    carray: cython.const[cython.Py_UCS4][1] = 'X'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_1_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_1_constant())
    ['X']
    """
    carray: cython.const[cython.Py_UCS4][1] = 'X'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_1_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_1_constant())
    ['X']
    """
    carray: cython.const[cython.Py_UCS4][1] = 'X'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_1_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_1_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_1_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_1_literal())
    ['X']
    """


    for item in 'X':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_1_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_1_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_1_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_1_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_1_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_1_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_1_pointer()
    ['X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'X'

    items = []
    for item in carray[:1]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_1_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_1_pointer())
    ['X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'X'

    for item in carray[:1]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_1_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_1_pointer()
    ['X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'X'

    return [item for item in carray[:1]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_1_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_1_pointer())
    ['X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'X'

    return {item for item in carray[:1]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_1_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_1_pointer())
    ['X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'X'

    return (item for item in carray[:1])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_7_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_7_constant()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.const[cython.Py_UCS4][7] = 'abc-def'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_7_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_7_constant())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.const[cython.Py_UCS4][7] = 'abc-def'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_7_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_7_constant()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.const[cython.Py_UCS4][7] = 'abc-def'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_7_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_7_constant())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """
    carray: cython.const[cython.Py_UCS4][7] = 'abc-def'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_7_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_7_constant())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.const[cython.Py_UCS4][7] = 'abc-def'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_7_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_7_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_7_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_7_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_7_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_7_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_7_pointer()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_7_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_7_pointer())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'abc-def'

    for item in carray[:7]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_7_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_7_pointer()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'abc-def'

    return [item for item in carray[:7]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_7_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_7_pointer())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'abc-def'

    return {item for item in carray[:7]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_7_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_7_pointer())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'abc-def'

    return (item for item in carray[:7])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_133_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_133_constant()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.const[cython.Py_UCS4][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_133_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_133_constant())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.const[cython.Py_UCS4][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_133_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_133_constant()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.const[cython.Py_UCS4][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_133_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_133_constant())
    ['X']
    """
    carray: cython.const[cython.Py_UCS4][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_133_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_133_constant())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.const[cython.Py_UCS4][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_133_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_133_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_133_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_133_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_133_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_133_pointer()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_133_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_133_pointer())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_133_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_133_pointer()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_133_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_133_pointer())
    ['X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_133_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_133_pointer())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_1_44_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_1_44_constant()
    ['☃']
    """
    carray: cython.const[cython.Py_UCS4][1] = '☃'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_1_44_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_1_44_constant())
    ['☃']
    """
    carray: cython.const[cython.Py_UCS4][1] = '☃'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_1_44_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_1_44_constant()
    ['☃']
    """
    carray: cython.const[cython.Py_UCS4][1] = '☃'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_1_44_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_1_44_constant())
    ['☃']
    """
    carray: cython.const[cython.Py_UCS4][1] = '☃'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_1_44_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_1_44_constant())
    ['☃']
    """
    carray: cython.const[cython.Py_UCS4][1] = '☃'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_1_44_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_1_44_literal()
    ['☃']
    """


    items = []
    for item in '☃':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_1_44_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_1_44_literal())
    ['☃']
    """


    for item in '☃':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_1_44_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_1_44_literal()
    ['☃']
    """


    return [item for item in '☃']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_1_44_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_1_44_literal())
    ['☃']
    """


    return {item for item in '☃'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_1_44_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_1_44_literal())
    ['☃']
    """


    return (item for item in '☃')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_1_44_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_1_44_pointer()
    ['☃']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '☃'

    items = []
    for item in carray[:1]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_1_44_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_1_44_pointer())
    ['☃']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '☃'

    for item in carray[:1]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_1_44_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_1_44_pointer()
    ['☃']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '☃'

    return [item for item in carray[:1]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_1_44_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_1_44_pointer())
    ['☃']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '☃'

    return {item for item in carray[:1]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_1_44_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_1_44_pointer())
    ['☃']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '☃'

    return (item for item in carray[:1])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_11_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_11_constant()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.const[cython.Py_UCS4][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_11_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_11_constant())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.const[cython.Py_UCS4][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_11_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_11_constant()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.const[cython.Py_UCS4][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_11_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_11_constant())
    ['∑']
    """
    carray: cython.const[cython.Py_UCS4][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_11_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_11_constant())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.const[cython.Py_UCS4][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_11_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    items = []
    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_11_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_11_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return [item for item in '∑∑∑∑∑∑∑∑∑∑∑']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_11_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_11_literal())
    ['∑']
    """


    return {item for item in '∑∑∑∑∑∑∑∑∑∑∑'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_11_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return (item for item in '∑∑∑∑∑∑∑∑∑∑∑')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_11_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_11_pointer()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray[:11]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_11_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_11_pointer())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray[:11]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_11_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_11_pointer()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray[:11]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_11_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_11_pointer())
    ['∑']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray[:11]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_11_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_11_pointer())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray[:11])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_21_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_21_constant()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.const[cython.Py_UCS4][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_21_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_21_constant())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.const[cython.Py_UCS4][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_21_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_21_constant()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.const[cython.Py_UCS4][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_21_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_21_constant())
    [' ', 'ℇ', '∑']
    """
    carray: cython.const[cython.Py_UCS4][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_21_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_21_constant())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.const[cython.Py_UCS4][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_21_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    items = []
    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_21_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_21_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return [item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_21_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_21_literal())
    [' ', 'ℇ', '∑']
    """


    return {item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_21_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return (item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_21_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_21_pointer()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray[:21]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_21_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_21_pointer())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray[:21]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_21_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_21_pointer()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray[:21]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_21_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_21_pointer())
    [' ', 'ℇ', '∑']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray[:21]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_21_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_21_pointer())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray[:21])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_2_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_2_constant()
    ['😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][2] = '😇😌'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_2_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_2_constant())
    ['😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][2] = '😇😌'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_2_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_2_constant()
    ['😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][2] = '😇😌'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_2_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_2_constant())
    ['😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][2] = '😇😌'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_2_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_2_constant())
    ['😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][2] = '😇😌'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_2_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_2_literal()
    ['😇', '😌']
    """


    items = []
    for item in '😇😌':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_2_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_2_literal())
    ['😇', '😌']
    """


    for item in '😇😌':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_2_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_2_literal()
    ['😇', '😌']
    """


    return [item for item in '😇😌']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_2_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_2_literal())
    ['😇', '😌']
    """


    return {item for item in '😇😌'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_2_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_2_literal())
    ['😇', '😌']
    """


    return (item for item in '😇😌')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_2_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_2_pointer()
    ['😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌'

    items = []
    for item in carray[:2]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_2_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_2_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌'

    for item in carray[:2]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_2_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_2_pointer()
    ['😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌'

    return [item for item in carray[:2]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_2_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_2_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌'

    return {item for item in carray[:2]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_2_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_2_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌'

    return (item for item in carray[:2])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_3_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_3_constant()
    ['😇', 'x', '😌']
    """
    carray: cython.const[cython.Py_UCS4][3] = '😇x😌'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_3_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_3_constant())
    ['😇', 'x', '😌']
    """
    carray: cython.const[cython.Py_UCS4][3] = '😇x😌'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_3_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_3_constant()
    ['😇', 'x', '😌']
    """
    carray: cython.const[cython.Py_UCS4][3] = '😇x😌'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_3_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_3_constant())
    ['x', '😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][3] = '😇x😌'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_3_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_3_constant())
    ['😇', 'x', '😌']
    """
    carray: cython.const[cython.Py_UCS4][3] = '😇x😌'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_3_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_3_literal()
    ['😇', 'x', '😌']
    """


    items = []
    for item in '😇x😌':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_3_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_3_literal())
    ['😇', 'x', '😌']
    """


    for item in '😇x😌':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_3_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_3_literal()
    ['😇', 'x', '😌']
    """


    return [item for item in '😇x😌']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_3_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_3_literal())
    ['x', '😇', '😌']
    """


    return {item for item in '😇x😌'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_3_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_3_literal())
    ['😇', 'x', '😌']
    """


    return (item for item in '😇x😌')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_3_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_3_pointer()
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇x😌'

    items = []
    for item in carray[:3]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_3_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_3_pointer())
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇x😌'

    for item in carray[:3]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_3_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_3_pointer()
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇x😌'

    return [item for item in carray[:3]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_3_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_3_pointer())
    ['x', '😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇x😌'

    return {item for item in carray[:3]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_3_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_3_pointer())
    ['😇', 'x', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇x😌'

    return (item for item in carray[:3])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_const_Py_UCS4_14_constant():
    """
    >>> test_carray_forin_constant_const_Py_UCS4_14_constant()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    items = []
    for item in carray:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_constant_const_Py_UCS4_14_constant():
    """
    >>> list(test_carray_generator_constant_const_Py_UCS4_14_constant())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    for item in carray:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_constant_const_Py_UCS4_14_constant():
    """
    >>> test_carray_listcomp_constant_const_Py_UCS4_14_constant()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return [item for item in carray]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_constant_const_Py_UCS4_14_constant():
    """
    >>> sorted(test_carray_setcomp_constant_const_Py_UCS4_14_constant())
    ['😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return {item for item in carray}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_constant_const_Py_UCS4_14_constant():
    """
    >>> list(test_carray_genexpr_constant_const_Py_UCS4_14_constant())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.const[cython.Py_UCS4][14] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return (item for item in carray)  # cython.const[cython.Py_UCS4]



def test_literal_forin_literal_const_Py_UCS4_14_literal():
    """
    >>> test_literal_forin_literal_const_Py_UCS4_14_literal()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    items = []
    for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌':  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_literal_generator_literal_const_Py_UCS4_14_literal():
    """
    >>> list(test_literal_generator_literal_const_Py_UCS4_14_literal())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌':  # cython.const[cython.Py_UCS4]
        yield item



def test_literal_listcomp_literal_const_Py_UCS4_14_literal():
    """
    >>> test_literal_listcomp_literal_const_Py_UCS4_14_literal()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    return [item for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌']  # cython.const[cython.Py_UCS4]



def test_literal_setcomp_literal_const_Py_UCS4_14_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_Py_UCS4_14_literal())
    ['😇', '😌']
    """


    return {item for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'}  # cython.const[cython.Py_UCS4]



def test_literal_genexpr_literal_const_Py_UCS4_14_literal():
    """
    >>> list(test_literal_genexpr_literal_const_Py_UCS4_14_literal())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """


    return (item for item in '😇😌😇😌😇😌😇😌😇😌😇😌😇😌')  # cython.const[cython.Py_UCS4]



def test_carray_forin_pointer_const_Py_UCS4_14_pointer():
    """
    >>> test_carray_forin_pointer_const_Py_UCS4_14_pointer()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    items = []
    for item in carray[:14]:  # cython.const[cython.Py_UCS4]
        items.append(item)
    return items



def test_carray_generator_pointer_const_Py_UCS4_14_pointer():
    """
    >>> list(test_carray_generator_pointer_const_Py_UCS4_14_pointer())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    for item in carray[:14]:  # cython.const[cython.Py_UCS4]
        yield item



def test_carray_listcomp_pointer_const_Py_UCS4_14_pointer():
    """
    >>> test_carray_listcomp_pointer_const_Py_UCS4_14_pointer()
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return [item for item in carray[:14]]  # cython.const[cython.Py_UCS4]



def test_carray_setcomp_pointer_const_Py_UCS4_14_pointer():
    """
    >>> sorted(test_carray_setcomp_pointer_const_Py_UCS4_14_pointer())
    ['😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return {item for item in carray[:14]}  # cython.const[cython.Py_UCS4]



def test_carray_genexpr_pointer_const_Py_UCS4_14_pointer():
    """
    >>> list(test_carray_genexpr_pointer_const_Py_UCS4_14_pointer())
    ['😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌', '😇', '😌']
    """
    carray: cython.pointer[cython.const[cython.Py_UCS4]] = '😇😌😇😌😇😌😇😌😇😌😇😌😇😌'

    return (item for item in carray[:14])  # cython.const[cython.Py_UCS4]



def test_carray_forin_constant_short_1_constant():
    """
    >>> charlist(test_carray_forin_constant_short_1_constant())
    [88]
    """
    carray: cython.short[1] = 'X'

    items = []
    for item in carray:  # cython.short
        items.append(item)
    return items



def test_carray_generator_constant_short_1_constant():
    """
    >>> charlist(list(test_carray_generator_constant_short_1_constant()))
    [88]
    """
    carray: cython.short[1] = 'X'

    for item in carray:  # cython.short
        yield item



def test_carray_listcomp_constant_short_1_constant():
    """
    >>> charlist(test_carray_listcomp_constant_short_1_constant())
    [88]
    """
    carray: cython.short[1] = 'X'

    return [item for item in carray]  # cython.short



def test_carray_setcomp_constant_short_1_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_short_1_constant()))
    [88]
    """
    carray: cython.short[1] = 'X'

    return {item for item in carray}  # cython.short



def test_carray_genexpr_constant_short_1_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_short_1_constant()))
    [88]
    """
    carray: cython.short[1] = 'X'

    return (item for item in carray)  # cython.short



def test_literal_forin_literal_short_1_literal():
    """
    >>> test_literal_forin_literal_short_1_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.short
        items.append(item)
    return items



def test_literal_generator_literal_short_1_literal():
    """
    >>> list(test_literal_generator_literal_short_1_literal())
    ['X']
    """


    for item in 'X':  # cython.short
        yield item



def test_literal_listcomp_literal_short_1_literal():
    """
    >>> test_literal_listcomp_literal_short_1_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.short



def test_literal_setcomp_literal_short_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_short_1_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.short



def test_literal_genexpr_literal_short_1_literal():
    """
    >>> list(test_literal_genexpr_literal_short_1_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.short



def test_carray_forin_pointer_short_1_pointer():
    """
    >>> charlist(test_carray_forin_pointer_short_1_pointer())
    [88]
    """
    carray: cython.pointer[cython.short] = 'X'

    items = []
    for item in carray[:1]:  # cython.short
        items.append(item)
    return items



def test_carray_generator_pointer_short_1_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_short_1_pointer()))
    [88]
    """
    carray: cython.pointer[cython.short] = 'X'

    for item in carray[:1]:  # cython.short
        yield item



def test_carray_listcomp_pointer_short_1_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_short_1_pointer())
    [88]
    """
    carray: cython.pointer[cython.short] = 'X'

    return [item for item in carray[:1]]  # cython.short



def test_carray_setcomp_pointer_short_1_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_short_1_pointer()))
    [88]
    """
    carray: cython.pointer[cython.short] = 'X'

    return {item for item in carray[:1]}  # cython.short



def test_carray_genexpr_pointer_short_1_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_short_1_pointer()))
    [88]
    """
    carray: cython.pointer[cython.short] = 'X'

    return (item for item in carray[:1])  # cython.short



def test_carray_forin_constant_short_7_constant():
    """
    >>> charlist(test_carray_forin_constant_short_7_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.short[7] = 'abc-def'

    items = []
    for item in carray:  # cython.short
        items.append(item)
    return items



def test_carray_generator_constant_short_7_constant():
    """
    >>> charlist(list(test_carray_generator_constant_short_7_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.short[7] = 'abc-def'

    for item in carray:  # cython.short
        yield item



def test_carray_listcomp_constant_short_7_constant():
    """
    >>> charlist(test_carray_listcomp_constant_short_7_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.short[7] = 'abc-def'

    return [item for item in carray]  # cython.short



def test_carray_setcomp_constant_short_7_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_short_7_constant()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.short[7] = 'abc-def'

    return {item for item in carray}  # cython.short



def test_carray_genexpr_constant_short_7_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_short_7_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.short[7] = 'abc-def'

    return (item for item in carray)  # cython.short



def test_literal_forin_literal_short_7_literal():
    """
    >>> test_literal_forin_literal_short_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.short
        items.append(item)
    return items



def test_literal_generator_literal_short_7_literal():
    """
    >>> list(test_literal_generator_literal_short_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.short
        yield item



def test_literal_listcomp_literal_short_7_literal():
    """
    >>> test_literal_listcomp_literal_short_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.short



def test_literal_setcomp_literal_short_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_short_7_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.short



def test_literal_genexpr_literal_short_7_literal():
    """
    >>> list(test_literal_genexpr_literal_short_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.short



def test_carray_forin_pointer_short_7_pointer():
    """
    >>> charlist(test_carray_forin_pointer_short_7_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.short] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.short
        items.append(item)
    return items



def test_carray_generator_pointer_short_7_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_short_7_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.short] = 'abc-def'

    for item in carray[:7]:  # cython.short
        yield item



def test_carray_listcomp_pointer_short_7_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_short_7_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.short] = 'abc-def'

    return [item for item in carray[:7]]  # cython.short



def test_carray_setcomp_pointer_short_7_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_short_7_pointer()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.pointer[cython.short] = 'abc-def'

    return {item for item in carray[:7]}  # cython.short



def test_carray_genexpr_pointer_short_7_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_short_7_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.short] = 'abc-def'

    return (item for item in carray[:7])  # cython.short



def test_carray_forin_constant_short_133_constant():
    """
    >>> charlist(test_carray_forin_constant_short_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.short[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.short
        items.append(item)
    return items



def test_carray_generator_constant_short_133_constant():
    """
    >>> charlist(list(test_carray_generator_constant_short_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.short[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.short
        yield item



def test_carray_listcomp_constant_short_133_constant():
    """
    >>> charlist(test_carray_listcomp_constant_short_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.short[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.short



def test_carray_setcomp_constant_short_133_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_short_133_constant()))
    [88]
    """
    carray: cython.short[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.short



def test_carray_genexpr_constant_short_133_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_short_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.short[133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.short



def test_literal_forin_literal_short_133_literal():
    """
    >>> test_literal_forin_literal_short_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.short
        items.append(item)
    return items



def test_literal_generator_literal_short_133_literal():
    """
    >>> list(test_literal_generator_literal_short_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.short
        yield item



def test_literal_listcomp_literal_short_133_literal():
    """
    >>> test_literal_listcomp_literal_short_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.short



def test_literal_setcomp_literal_short_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_short_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.short



def test_literal_genexpr_literal_short_133_literal():
    """
    >>> list(test_literal_genexpr_literal_short_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.short



def test_carray_forin_pointer_short_133_pointer():
    """
    >>> charlist(test_carray_forin_pointer_short_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.short] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.short
        items.append(item)
    return items



def test_carray_generator_pointer_short_133_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_short_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.short] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.short
        yield item



def test_carray_listcomp_pointer_short_133_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_short_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.short] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.short



def test_carray_setcomp_pointer_short_133_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_short_133_pointer()))
    [88]
    """
    carray: cython.pointer[cython.short] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.short



def test_carray_genexpr_pointer_short_133_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_short_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.short] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.short



def test_carray_forin_constant_short_1_53_constant():
    """
    >>> charlist(test_carray_forin_constant_short_1_53_constant())
    [9731]
    """
    carray: cython.short[1] = '☃'

    items = []
    for item in carray:  # cython.short
        items.append(item)
    return items



def test_carray_generator_constant_short_1_53_constant():
    """
    >>> charlist(list(test_carray_generator_constant_short_1_53_constant()))
    [9731]
    """
    carray: cython.short[1] = '☃'

    for item in carray:  # cython.short
        yield item



def test_carray_listcomp_constant_short_1_53_constant():
    """
    >>> charlist(test_carray_listcomp_constant_short_1_53_constant())
    [9731]
    """
    carray: cython.short[1] = '☃'

    return [item for item in carray]  # cython.short



def test_carray_setcomp_constant_short_1_53_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_short_1_53_constant()))
    [9731]
    """
    carray: cython.short[1] = '☃'

    return {item for item in carray}  # cython.short



def test_carray_genexpr_constant_short_1_53_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_short_1_53_constant()))
    [9731]
    """
    carray: cython.short[1] = '☃'

    return (item for item in carray)  # cython.short



def test_literal_forin_literal_short_1_53_literal():
    """
    >>> test_literal_forin_literal_short_1_53_literal()
    ['☃']
    """


    items = []
    for item in '☃':  # cython.short
        items.append(item)
    return items



def test_literal_generator_literal_short_1_53_literal():
    """
    >>> list(test_literal_generator_literal_short_1_53_literal())
    ['☃']
    """


    for item in '☃':  # cython.short
        yield item



def test_literal_listcomp_literal_short_1_53_literal():
    """
    >>> test_literal_listcomp_literal_short_1_53_literal()
    ['☃']
    """


    return [item for item in '☃']  # cython.short



def test_literal_setcomp_literal_short_1_53_literal():
    """
    >>> sorted(test_literal_setcomp_literal_short_1_53_literal())
    ['☃']
    """


    return {item for item in '☃'}  # cython.short



def test_literal_genexpr_literal_short_1_53_literal():
    """
    >>> list(test_literal_genexpr_literal_short_1_53_literal())
    ['☃']
    """


    return (item for item in '☃')  # cython.short



def test_carray_forin_pointer_short_1_53_pointer():
    """
    >>> charlist(test_carray_forin_pointer_short_1_53_pointer())
    [9731]
    """
    carray: cython.pointer[cython.short] = '☃'

    items = []
    for item in carray[:1]:  # cython.short
        items.append(item)
    return items



def test_carray_generator_pointer_short_1_53_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_short_1_53_pointer()))
    [9731]
    """
    carray: cython.pointer[cython.short] = '☃'

    for item in carray[:1]:  # cython.short
        yield item



def test_carray_listcomp_pointer_short_1_53_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_short_1_53_pointer())
    [9731]
    """
    carray: cython.pointer[cython.short] = '☃'

    return [item for item in carray[:1]]  # cython.short



def test_carray_setcomp_pointer_short_1_53_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_short_1_53_pointer()))
    [9731]
    """
    carray: cython.pointer[cython.short] = '☃'

    return {item for item in carray[:1]}  # cython.short



def test_carray_genexpr_pointer_short_1_53_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_short_1_53_pointer()))
    [9731]
    """
    carray: cython.pointer[cython.short] = '☃'

    return (item for item in carray[:1])  # cython.short



def test_carray_forin_constant_short_11_constant():
    """
    >>> charlist(test_carray_forin_constant_short_11_constant())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.short[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray:  # cython.short
        items.append(item)
    return items



def test_carray_generator_constant_short_11_constant():
    """
    >>> charlist(list(test_carray_generator_constant_short_11_constant()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.short[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray:  # cython.short
        yield item



def test_carray_listcomp_constant_short_11_constant():
    """
    >>> charlist(test_carray_listcomp_constant_short_11_constant())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.short[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray]  # cython.short



def test_carray_setcomp_constant_short_11_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_short_11_constant()))
    [8721]
    """
    carray: cython.short[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray}  # cython.short



def test_carray_genexpr_constant_short_11_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_short_11_constant()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.short[11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray)  # cython.short



def test_literal_forin_literal_short_11_literal():
    """
    >>> test_literal_forin_literal_short_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    items = []
    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.short
        items.append(item)
    return items



def test_literal_generator_literal_short_11_literal():
    """
    >>> list(test_literal_generator_literal_short_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.short
        yield item



def test_literal_listcomp_literal_short_11_literal():
    """
    >>> test_literal_listcomp_literal_short_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return [item for item in '∑∑∑∑∑∑∑∑∑∑∑']  # cython.short



def test_literal_setcomp_literal_short_11_literal():
    """
    >>> sorted(test_literal_setcomp_literal_short_11_literal())
    ['∑']
    """


    return {item for item in '∑∑∑∑∑∑∑∑∑∑∑'}  # cython.short



def test_literal_genexpr_literal_short_11_literal():
    """
    >>> list(test_literal_genexpr_literal_short_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return (item for item in '∑∑∑∑∑∑∑∑∑∑∑')  # cython.short



def test_carray_forin_pointer_short_11_pointer():
    """
    >>> charlist(test_carray_forin_pointer_short_11_pointer())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.short] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray[:11]:  # cython.short
        items.append(item)
    return items



def test_carray_generator_pointer_short_11_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_short_11_pointer()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.short] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray[:11]:  # cython.short
        yield item



def test_carray_listcomp_pointer_short_11_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_short_11_pointer())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.short] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray[:11]]  # cython.short



def test_carray_setcomp_pointer_short_11_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_short_11_pointer()))
    [8721]
    """
    carray: cython.pointer[cython.short] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray[:11]}  # cython.short



def test_carray_genexpr_pointer_short_11_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_short_11_pointer()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.short] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray[:11])  # cython.short



def test_carray_forin_constant_short_21_constant():
    """
    >>> charlist(test_carray_forin_constant_short_21_constant())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.short[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray:  # cython.short
        items.append(item)
    return items



def test_carray_generator_constant_short_21_constant():
    """
    >>> charlist(list(test_carray_generator_constant_short_21_constant()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.short[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray:  # cython.short
        yield item



def test_carray_listcomp_constant_short_21_constant():
    """
    >>> charlist(test_carray_listcomp_constant_short_21_constant())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.short[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray]  # cython.short



def test_carray_setcomp_constant_short_21_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_short_21_constant()))
    [32, 8455, 8721]
    """
    carray: cython.short[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray}  # cython.short



def test_carray_genexpr_constant_short_21_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_short_21_constant()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.short[21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray)  # cython.short



def test_literal_forin_literal_short_21_literal():
    """
    >>> test_literal_forin_literal_short_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    items = []
    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.short
        items.append(item)
    return items



def test_literal_generator_literal_short_21_literal():
    """
    >>> list(test_literal_generator_literal_short_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.short
        yield item



def test_literal_listcomp_literal_short_21_literal():
    """
    >>> test_literal_listcomp_literal_short_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return [item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ']  # cython.short



def test_literal_setcomp_literal_short_21_literal():
    """
    >>> sorted(test_literal_setcomp_literal_short_21_literal())
    [' ', 'ℇ', '∑']
    """


    return {item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'}  # cython.short



def test_literal_genexpr_literal_short_21_literal():
    """
    >>> list(test_literal_genexpr_literal_short_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return (item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ')  # cython.short



def test_carray_forin_pointer_short_21_pointer():
    """
    >>> charlist(test_carray_forin_pointer_short_21_pointer())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.short] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray[:21]:  # cython.short
        items.append(item)
    return items



def test_carray_generator_pointer_short_21_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_short_21_pointer()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.short] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray[:21]:  # cython.short
        yield item



def test_carray_listcomp_pointer_short_21_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_short_21_pointer())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.short] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray[:21]]  # cython.short



def test_carray_setcomp_pointer_short_21_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_short_21_pointer()))
    [32, 8455, 8721]
    """
    carray: cython.pointer[cython.short] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray[:21]}  # cython.short



def test_carray_genexpr_pointer_short_21_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_short_21_pointer()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.short] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray[:21])  # cython.short



def test_carray_forin_constant_const_short_1_constant():
    """
    >>> charlist(test_carray_forin_constant_const_short_1_constant())
    [88]
    """
    carray: cython.const[cython.short][1] = 'X'

    items = []
    for item in carray:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_constant_const_short_1_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_short_1_constant()))
    [88]
    """
    carray: cython.const[cython.short][1] = 'X'

    for item in carray:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_constant_const_short_1_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_short_1_constant())
    [88]
    """
    carray: cython.const[cython.short][1] = 'X'

    return [item for item in carray]  # cython.const[cython.short]



def test_carray_setcomp_constant_const_short_1_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_short_1_constant()))
    [88]
    """
    carray: cython.const[cython.short][1] = 'X'

    return {item for item in carray}  # cython.const[cython.short]



def test_carray_genexpr_constant_const_short_1_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_short_1_constant()))
    [88]
    """
    carray: cython.const[cython.short][1] = 'X'

    return (item for item in carray)  # cython.const[cython.short]



def test_literal_forin_literal_const_short_1_literal():
    """
    >>> test_literal_forin_literal_const_short_1_literal()
    ['X']
    """


    items = []
    for item in 'X':  # cython.const[cython.short]
        items.append(item)
    return items



def test_literal_generator_literal_const_short_1_literal():
    """
    >>> list(test_literal_generator_literal_const_short_1_literal())
    ['X']
    """


    for item in 'X':  # cython.const[cython.short]
        yield item



def test_literal_listcomp_literal_const_short_1_literal():
    """
    >>> test_literal_listcomp_literal_const_short_1_literal()
    ['X']
    """


    return [item for item in 'X']  # cython.const[cython.short]



def test_literal_setcomp_literal_const_short_1_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_short_1_literal())
    ['X']
    """


    return {item for item in 'X'}  # cython.const[cython.short]



def test_literal_genexpr_literal_const_short_1_literal():
    """
    >>> list(test_literal_genexpr_literal_const_short_1_literal())
    ['X']
    """


    return (item for item in 'X')  # cython.const[cython.short]



def test_carray_forin_pointer_const_short_1_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_short_1_pointer())
    [88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'X'

    items = []
    for item in carray[:1]:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_pointer_const_short_1_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_short_1_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'X'

    for item in carray[:1]:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_pointer_const_short_1_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_short_1_pointer())
    [88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'X'

    return [item for item in carray[:1]]  # cython.const[cython.short]



def test_carray_setcomp_pointer_const_short_1_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_short_1_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'X'

    return {item for item in carray[:1]}  # cython.const[cython.short]



def test_carray_genexpr_pointer_const_short_1_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_short_1_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'X'

    return (item for item in carray[:1])  # cython.const[cython.short]



def test_carray_forin_constant_const_short_7_constant():
    """
    >>> charlist(test_carray_forin_constant_const_short_7_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.short][7] = 'abc-def'

    items = []
    for item in carray:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_constant_const_short_7_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_short_7_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.short][7] = 'abc-def'

    for item in carray:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_constant_const_short_7_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_short_7_constant())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.short][7] = 'abc-def'

    return [item for item in carray]  # cython.const[cython.short]



def test_carray_setcomp_constant_const_short_7_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_short_7_constant()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.const[cython.short][7] = 'abc-def'

    return {item for item in carray}  # cython.const[cython.short]



def test_carray_genexpr_constant_const_short_7_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_short_7_constant()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.const[cython.short][7] = 'abc-def'

    return (item for item in carray)  # cython.const[cython.short]



def test_literal_forin_literal_const_short_7_literal():
    """
    >>> test_literal_forin_literal_const_short_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    items = []
    for item in 'abc-def':  # cython.const[cython.short]
        items.append(item)
    return items



def test_literal_generator_literal_const_short_7_literal():
    """
    >>> list(test_literal_generator_literal_const_short_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    for item in 'abc-def':  # cython.const[cython.short]
        yield item



def test_literal_listcomp_literal_const_short_7_literal():
    """
    >>> test_literal_listcomp_literal_const_short_7_literal()
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return [item for item in 'abc-def']  # cython.const[cython.short]



def test_literal_setcomp_literal_const_short_7_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_short_7_literal())
    ['-', 'a', 'b', 'c', 'd', 'e', 'f']
    """


    return {item for item in 'abc-def'}  # cython.const[cython.short]



def test_literal_genexpr_literal_const_short_7_literal():
    """
    >>> list(test_literal_genexpr_literal_const_short_7_literal())
    ['a', 'b', 'c', '-', 'd', 'e', 'f']
    """


    return (item for item in 'abc-def')  # cython.const[cython.short]



def test_carray_forin_pointer_const_short_7_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_short_7_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'abc-def'

    items = []
    for item in carray[:7]:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_pointer_const_short_7_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_short_7_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'abc-def'

    for item in carray[:7]:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_pointer_const_short_7_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_short_7_pointer())
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'abc-def'

    return [item for item in carray[:7]]  # cython.const[cython.short]



def test_carray_setcomp_pointer_const_short_7_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_short_7_pointer()))
    [45, 97, 98, 99, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'abc-def'

    return {item for item in carray[:7]}  # cython.const[cython.short]



def test_carray_genexpr_pointer_const_short_7_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_short_7_pointer()))
    [97, 98, 99, 45, 100, 101, 102]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'abc-def'

    return (item for item in carray[:7])  # cython.const[cython.short]



def test_carray_forin_constant_const_short_133_constant():
    """
    >>> charlist(test_carray_forin_constant_const_short_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.short][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_constant_const_short_133_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_short_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.short][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_constant_const_short_133_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_short_133_constant())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.short][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray]  # cython.const[cython.short]



def test_carray_setcomp_constant_const_short_133_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_short_133_constant()))
    [88]
    """
    carray: cython.const[cython.short][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray}  # cython.const[cython.short]



def test_carray_genexpr_constant_const_short_133_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_short_133_constant()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.const[cython.short][133] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray)  # cython.const[cython.short]



def test_literal_forin_literal_const_short_133_literal():
    """
    >>> test_literal_forin_literal_const_short_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    items = []
    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.short]
        items.append(item)
    return items



def test_literal_generator_literal_const_short_133_literal():
    """
    >>> list(test_literal_generator_literal_const_short_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':  # cython.const[cython.short]
        yield item



def test_literal_listcomp_literal_const_short_133_literal():
    """
    >>> test_literal_listcomp_literal_const_short_133_literal()
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return [item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']  # cython.const[cython.short]



def test_literal_setcomp_literal_const_short_133_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_short_133_literal())
    ['X']
    """


    return {item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}  # cython.const[cython.short]



def test_literal_genexpr_literal_const_short_133_literal():
    """
    >>> list(test_literal_genexpr_literal_const_short_133_literal())
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    """


    return (item for item in 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # cython.const[cython.short]



def test_carray_forin_pointer_const_short_133_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_short_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    items = []
    for item in carray[:133]:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_pointer_const_short_133_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_short_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for item in carray[:133]:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_pointer_const_short_133_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_short_133_pointer())
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return [item for item in carray[:133]]  # cython.const[cython.short]



def test_carray_setcomp_pointer_const_short_133_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_short_133_pointer()))
    [88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return {item for item in carray[:133]}  # cython.const[cython.short]



def test_carray_genexpr_pointer_const_short_133_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_short_133_pointer()))
    [88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
    """
    carray: cython.pointer[cython.const[cython.short]] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    return (item for item in carray[:133])  # cython.const[cython.short]



def test_carray_forin_constant_const_short_1_59_constant():
    """
    >>> charlist(test_carray_forin_constant_const_short_1_59_constant())
    [9731]
    """
    carray: cython.const[cython.short][1] = '☃'

    items = []
    for item in carray:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_constant_const_short_1_59_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_short_1_59_constant()))
    [9731]
    """
    carray: cython.const[cython.short][1] = '☃'

    for item in carray:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_constant_const_short_1_59_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_short_1_59_constant())
    [9731]
    """
    carray: cython.const[cython.short][1] = '☃'

    return [item for item in carray]  # cython.const[cython.short]



def test_carray_setcomp_constant_const_short_1_59_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_short_1_59_constant()))
    [9731]
    """
    carray: cython.const[cython.short][1] = '☃'

    return {item for item in carray}  # cython.const[cython.short]



def test_carray_genexpr_constant_const_short_1_59_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_short_1_59_constant()))
    [9731]
    """
    carray: cython.const[cython.short][1] = '☃'

    return (item for item in carray)  # cython.const[cython.short]



def test_literal_forin_literal_const_short_1_59_literal():
    """
    >>> test_literal_forin_literal_const_short_1_59_literal()
    ['☃']
    """


    items = []
    for item in '☃':  # cython.const[cython.short]
        items.append(item)
    return items



def test_literal_generator_literal_const_short_1_59_literal():
    """
    >>> list(test_literal_generator_literal_const_short_1_59_literal())
    ['☃']
    """


    for item in '☃':  # cython.const[cython.short]
        yield item



def test_literal_listcomp_literal_const_short_1_59_literal():
    """
    >>> test_literal_listcomp_literal_const_short_1_59_literal()
    ['☃']
    """


    return [item for item in '☃']  # cython.const[cython.short]



def test_literal_setcomp_literal_const_short_1_59_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_short_1_59_literal())
    ['☃']
    """


    return {item for item in '☃'}  # cython.const[cython.short]



def test_literal_genexpr_literal_const_short_1_59_literal():
    """
    >>> list(test_literal_genexpr_literal_const_short_1_59_literal())
    ['☃']
    """


    return (item for item in '☃')  # cython.const[cython.short]



def test_carray_forin_pointer_const_short_1_59_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_short_1_59_pointer())
    [9731]
    """
    carray: cython.pointer[cython.const[cython.short]] = '☃'

    items = []
    for item in carray[:1]:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_pointer_const_short_1_59_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_short_1_59_pointer()))
    [9731]
    """
    carray: cython.pointer[cython.const[cython.short]] = '☃'

    for item in carray[:1]:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_pointer_const_short_1_59_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_short_1_59_pointer())
    [9731]
    """
    carray: cython.pointer[cython.const[cython.short]] = '☃'

    return [item for item in carray[:1]]  # cython.const[cython.short]



def test_carray_setcomp_pointer_const_short_1_59_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_short_1_59_pointer()))
    [9731]
    """
    carray: cython.pointer[cython.const[cython.short]] = '☃'

    return {item for item in carray[:1]}  # cython.const[cython.short]



def test_carray_genexpr_pointer_const_short_1_59_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_short_1_59_pointer()))
    [9731]
    """
    carray: cython.pointer[cython.const[cython.short]] = '☃'

    return (item for item in carray[:1])  # cython.const[cython.short]



def test_carray_forin_constant_const_short_11_constant():
    """
    >>> charlist(test_carray_forin_constant_const_short_11_constant())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.const[cython.short][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_constant_const_short_11_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_short_11_constant()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.const[cython.short][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_constant_const_short_11_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_short_11_constant())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.const[cython.short][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray]  # cython.const[cython.short]



def test_carray_setcomp_constant_const_short_11_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_short_11_constant()))
    [8721]
    """
    carray: cython.const[cython.short][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray}  # cython.const[cython.short]



def test_carray_genexpr_constant_const_short_11_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_short_11_constant()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.const[cython.short][11] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray)  # cython.const[cython.short]



def test_literal_forin_literal_const_short_11_literal():
    """
    >>> test_literal_forin_literal_const_short_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    items = []
    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.const[cython.short]
        items.append(item)
    return items



def test_literal_generator_literal_const_short_11_literal():
    """
    >>> list(test_literal_generator_literal_const_short_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    for item in '∑∑∑∑∑∑∑∑∑∑∑':  # cython.const[cython.short]
        yield item



def test_literal_listcomp_literal_const_short_11_literal():
    """
    >>> test_literal_listcomp_literal_const_short_11_literal()
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return [item for item in '∑∑∑∑∑∑∑∑∑∑∑']  # cython.const[cython.short]



def test_literal_setcomp_literal_const_short_11_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_short_11_literal())
    ['∑']
    """


    return {item for item in '∑∑∑∑∑∑∑∑∑∑∑'}  # cython.const[cython.short]



def test_literal_genexpr_literal_const_short_11_literal():
    """
    >>> list(test_literal_genexpr_literal_const_short_11_literal())
    ['∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑', '∑']
    """


    return (item for item in '∑∑∑∑∑∑∑∑∑∑∑')  # cython.const[cython.short]



def test_carray_forin_pointer_const_short_11_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_short_11_pointer())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑∑∑∑∑∑∑∑∑∑∑'

    items = []
    for item in carray[:11]:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_pointer_const_short_11_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_short_11_pointer()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑∑∑∑∑∑∑∑∑∑∑'

    for item in carray[:11]:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_pointer_const_short_11_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_short_11_pointer())
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑∑∑∑∑∑∑∑∑∑∑'

    return [item for item in carray[:11]]  # cython.const[cython.short]



def test_carray_setcomp_pointer_const_short_11_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_short_11_pointer()))
    [8721]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑∑∑∑∑∑∑∑∑∑∑'

    return {item for item in carray[:11]}  # cython.const[cython.short]



def test_carray_genexpr_pointer_const_short_11_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_short_11_pointer()))
    [8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721, 8721]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑∑∑∑∑∑∑∑∑∑∑'

    return (item for item in carray[:11])  # cython.const[cython.short]



def test_carray_forin_constant_const_short_21_constant():
    """
    >>> charlist(test_carray_forin_constant_const_short_21_constant())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.const[cython.short][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_constant_const_short_21_constant():
    """
    >>> charlist(list(test_carray_generator_constant_const_short_21_constant()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.const[cython.short][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_constant_const_short_21_constant():
    """
    >>> charlist(test_carray_listcomp_constant_const_short_21_constant())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.const[cython.short][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray]  # cython.const[cython.short]



def test_carray_setcomp_constant_const_short_21_constant():
    """
    >>> charlist(sorted(test_carray_setcomp_constant_const_short_21_constant()))
    [32, 8455, 8721]
    """
    carray: cython.const[cython.short][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray}  # cython.const[cython.short]



def test_carray_genexpr_constant_const_short_21_constant():
    """
    >>> charlist(list(test_carray_genexpr_constant_const_short_21_constant()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.const[cython.short][21] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray)  # cython.const[cython.short]



def test_literal_forin_literal_const_short_21_literal():
    """
    >>> test_literal_forin_literal_const_short_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    items = []
    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.const[cython.short]
        items.append(item)
    return items



def test_literal_generator_literal_const_short_21_literal():
    """
    >>> list(test_literal_generator_literal_const_short_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ':  # cython.const[cython.short]
        yield item



def test_literal_listcomp_literal_const_short_21_literal():
    """
    >>> test_literal_listcomp_literal_const_short_21_literal()
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return [item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ']  # cython.const[cython.short]



def test_literal_setcomp_literal_const_short_21_literal():
    """
    >>> sorted(test_literal_setcomp_literal_const_short_21_literal())
    [' ', 'ℇ', '∑']
    """


    return {item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'}  # cython.const[cython.short]



def test_literal_genexpr_literal_const_short_21_literal():
    """
    >>> list(test_literal_genexpr_literal_const_short_21_literal())
    ['∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ', '∑', ' ', 'ℇ']
    """


    return (item for item in '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ')  # cython.const[cython.short]



def test_carray_forin_pointer_const_short_21_pointer():
    """
    >>> charlist(test_carray_forin_pointer_const_short_21_pointer())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    items = []
    for item in carray[:21]:  # cython.const[cython.short]
        items.append(item)
    return items



def test_carray_generator_pointer_const_short_21_pointer():
    """
    >>> charlist(list(test_carray_generator_pointer_const_short_21_pointer()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    for item in carray[:21]:  # cython.const[cython.short]
        yield item



def test_carray_listcomp_pointer_const_short_21_pointer():
    """
    >>> charlist(test_carray_listcomp_pointer_const_short_21_pointer())
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return [item for item in carray[:21]]  # cython.const[cython.short]



def test_carray_setcomp_pointer_const_short_21_pointer():
    """
    >>> charlist(sorted(test_carray_setcomp_pointer_const_short_21_pointer()))
    [32, 8455, 8721]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return {item for item in carray[:21]}  # cython.const[cython.short]



def test_carray_genexpr_pointer_const_short_21_pointer():
    """
    >>> charlist(list(test_carray_genexpr_pointer_const_short_21_pointer()))
    [8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455, 8721, 32, 8455]
    """
    carray: cython.pointer[cython.const[cython.short]] = '∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ∑ ℇ'

    return (item for item in carray[:21])  # cython.const[cython.short]

###### END: generated test code ######


#################################################
##  This is the test code generator script:
#################################################

def _gen_test_code():
    char_constants = [
        b'x',
        b'abcdefg',
        b'x' * 100,
    ]
    text_constants = [
        'X',
        'abc-def',
        'X' * 133,
    ]
    unicode_bmp_constants = [
        '\N{SNOWMAN}',
        '\N{N-ARY SUMMATION}' * 11,
        '\N{N-ARY SUMMATION} \N{EULER CONSTANT}' * 7,
    ]
    unicode_constants = [
        '\N{SMILING FACE WITH HALO}\N{RELIEVED FACE}',
        '\N{SMILING FACE WITH HALO}x\N{RELIEVED FACE}',
        '\N{SMILING FACE WITH HALO}\N{RELIEVED FACE}' * 7,
    ]
    int_constants = [
        [0],
        [0, 0],
        list(range(1, 5)),
        list(range(-133, 133)),
    ]

    constants = {
        'cython.int': int_constants,
        'cython.const[cython.int]': int_constants,
        'cython.char': char_constants + text_constants,
        'cython.const[cython.char]': char_constants + text_constants,
        'cython.uchar': char_constants + text_constants,
        'cython.const[cython.uchar]': char_constants + text_constants,
        'cython.Py_UCS4': text_constants + unicode_bmp_constants + unicode_constants,
        'cython.const[cython.Py_UCS4]': text_constants + unicode_bmp_constants + unicode_constants,
        'cython.short': text_constants + unicode_bmp_constants,
        'cython.const[cython.short]': text_constants + unicode_bmp_constants,
    }

    test_functions = []
    names_seen = set()
    unique_function_names = set()
    stats = dict(
        optimised=0,
        not_optimised=0,
    )
    from textwrap import dedent

    def function_header(test_variant, function_name, array_values, carray_decl=None, arg=None):
        function_name = f"test_{'carray' if carray_decl else 'literal'}_{test_variant}_{function_name}"

        assert function_name not in unique_function_names, function_name
        unique_function_names.add(function_name)

        optimised = True
        test_decorator = '@cython.test_assert_path_exists("//CArrayNode")'
        if carray_decl:
            if 'cython.pointer[' in carray_decl:
                test_decorator = '@cython.test_fail_if_path_exists("//IteratorNode//CArrayNode")'
                optimised = False
        elif not isinstance(array_values, (str, bytes)):
            test_decorator = '@cython.test_fail_if_path_exists("//CArrayNode")'
            optimised = False
        else:
            test_decorator = '@cython.test_assert_path_exists("//CArrayNode")'

        if optimised:
            stats['optimised'] += 1
        else:
            # Notify us when we start supporting something previously unsupported by carray iteration.
            test_decorator = '@cython.test_fail_if_path_exists("//CArrayNode")'
            stats['not_optimised'] += 1

        # FIXME: disabled until it's clear what we can support.
        test_decorator = ''

        needs_py_conversion = False
        if carray_decl and isinstance(array_values, str):
            if 'cython.short' in carray_decl or 'cython.uchar' in carray_decl or 'cython.char' in carray_decl:
                array_values = map(ord, array_values)
                needs_py_conversion = True

        test_call = f"{function_name}({arg or ''})"
        if 'setcomp' in test_variant:
            array_values = sorted(set(array_values))
            test_call = f"sorted({test_call})"
        elif 'generator' in test_variant or 'genexpr' in test_variant:
            array_values = list(array_values)
            test_call = f"list({test_call})"
        else:
            array_values = list(array_values)

        if needs_py_conversion:
            test_call = f"charlist({test_call})"

        return f'''
                {test_decorator}
                def {function_name}({'arg: cython.int' if arg is not None else ''}):
                    """
                    >>> {test_call}
                    {array_values!r}
                    """
                    {carray_decl or ''}
                    '''

    def gen_test_functions(item_type, array_values):
        item_type_name = item_type.replace('cython.', '').replace('[', '_').replace(']', '')
        function_name = f"{item_type_name}_{len(array_values)}"
        if function_name in names_seen:
            function_name += f"_{len(names_seen)}"
        names_seen.add(function_name)

        class DynamicLastArg:
            def __repr__(self):
                return 'arg'
            def __lt__(self, other):
                return False  # always sort last
            def __gt__(self, other):
                return True  # always sort last

        dynamic_last_arg = [DynamicLastArg()]

        test_matrix = [
            (array_kind, dynamic_arg)
            for array_kind in ('constant', 'literal', 'pointer')
            for dynamic_arg in ((4, None) if 'cython.int' in item_type else (None,))
        ]

        for array_kind, dynamic_arg in test_matrix:
            if dynamic_arg:
                test_values = array_values[:] + dynamic_last_arg
                test_result = array_values[:] + [dynamic_arg]
            else:
                test_values = array_values
                test_result = array_values

            if array_kind == 'constant':
                carray_decl = f"carray: {item_type}[{len(test_values)}] = {test_values!r}"
                carray = 'carray'
            elif array_kind == 'literal':
                carray_decl = None
                carray = f"{test_values!r}"
            elif array_kind == 'pointer':
                carray_decl = f"carray: cython.pointer[{item_type}] = {test_values!r}"
                carray = f"carray[:{len(test_values)}]"
            else:
                assert False, array_kind

            matrix_function_name = f"{function_name}_{array_kind}{'_arg' if dynamic_arg else ''}"

            test_functions.append(dedent(f'''\
                {function_header(f"forin_{array_kind}", matrix_function_name, test_result, carray_decl=carray_decl, arg=dynamic_arg)}
                    items = []
                    for item in {carray}:  # {item_type}
                        items.append(item)
                    return items

                {function_header(f"generator_{array_kind}", matrix_function_name, test_result, carray_decl=carray_decl, arg=dynamic_arg)}
                    for item in {carray}:  # {item_type}
                        yield item

                {function_header(f"listcomp_{array_kind}", matrix_function_name, test_result, carray_decl=carray_decl, arg=dynamic_arg)}
                    return [item for item in {carray}]  # {item_type}

                {function_header(f"setcomp_{array_kind}", matrix_function_name, test_result, carray_decl=carray_decl, arg=dynamic_arg)}
                    return {{item for item in {carray}}}  # {item_type}

                {function_header(f"genexpr_{array_kind}", matrix_function_name, test_result, carray_decl=carray_decl, arg=dynamic_arg)}
                    return (item for item in {carray})  # {item_type}

            '''))

    for constant_type, array_constants in constants.items():
        for array_values in array_constants:
            gen_test_functions(constant_type, array_values)

    stats_lines = [
        f"# {stats['optimised']:4d} tests optimised using CArrayNode\n",
        f"# {stats['not_optimised']:4d} tests not optimised\n",
    ]

    return test_functions, stats_lines


def _regen_test_file(file_path):
    with open(file_path) as f:
        lines = iter(f)
        start_lines = []
        end_lines = []
        for line in lines:
            start_lines.append(line)
            if line.startswith('###### ') and 'START' in line:
                break
        for line in lines:
            if line.startswith('###### ') and 'END' in line:
                end_lines.append(line)
                break
        end_lines.extend(lines)

    code, stats = _gen_test_code()

    from itertools import chain
    with open(file_path, 'w') as f:
        f.writelines(chain(start_lines, stats, code, end_lines))


if __name__ == '__main__':
    _regen_test_file(__file__)
