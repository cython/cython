# mode: run
# tag: carray, forin, genexpr, generators, comprehension, bytes, unicode

# Tests marked with "@cython.test_fail_if_path_exists()" are not currently optimised (but might be later.)

cimport cython


cdef extern from *:
    """
    typedef enum {
        EXT_ENUM_VALUE = 5,
    } ExtEnum;
    """
    enum ExtEnum:
        EXT_ENUM_VALUE

cdef enum InternalEnum:
    INTERNAL_ENUM_VALUE = 5


# Externally defined enum

@cython.test_assert_path_exists("//CArrayNode")
def test_carray_forin_ext_enum_typing():
    """
    >>> test_carray_forin_ext_enum_typing()
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[EXT_ENUM_VALUE] = [0, 1, 2, 3, 4]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_forin_ext_enum_cdef():
    """
    >>> test_carray_forin_ext_enum_cdef()
    [0, 1, 2, 3, 4]
    """
    cdef int[EXT_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_generator_ext_enum_typing():
    """
    >>> list(test_carray_generator_ext_enum_typing())
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[EXT_ENUM_VALUE] = [0, 1, 2, 3, 4]

    for item in carray:  # cython.int
        yield item


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_generator_ext_enum_cdef():
    """
    >>> list(test_carray_generator_ext_enum_cdef())
    [0, 1, 2, 3, 4]
    """
    cdef int[EXT_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    for item in carray:  # cython.int
        yield item


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_listcomp_ext_enum_typing():
    """
    >>> test_carray_listcomp_ext_enum_typing()
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[EXT_ENUM_VALUE] = [0, 1, 2, 3, 4]

    return [item for item in carray]  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_listcomp_ext_enum_cdef():
    """
    >>> test_carray_listcomp_ext_enum_cdef()
    [0, 1, 2, 3, 4]
    """
    cdef int[EXT_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    return [item for item in carray]  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_setcomp_ext_enum_typing():
    """
    >>> sorted(test_carray_setcomp_ext_enum_typing())
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[EXT_ENUM_VALUE] = [0, 1, 2, 3, 4]

    return {item for item in carray}  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_setcomp_ext_enum_cdef():
    """
    >>> sorted(test_carray_setcomp_ext_enum_cdef())
    [0, 1, 2, 3, 4]
    """
    cdef int[EXT_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    return {item for item in carray}  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_genexpr_ext_enum_typing():
    """
    >>> list(test_carray_genexpr_ext_enum_typing())
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[EXT_ENUM_VALUE] = [0, 1, 2, 3, 4]

    return (item for item in carray)  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_genexpr_ext_enum_cdef():
    """
    >>> list(test_carray_genexpr_ext_enum_cdef())
    [0, 1, 2, 3, 4]
    """
    cdef int[EXT_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    return (item for item in carray)  # cython.int


# Internally defined enum

@cython.test_assert_path_exists("//CArrayNode")
def test_carray_forin_enum_typing():
    """
    >>> test_carray_forin_enum_typing()
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[INTERNAL_ENUM_VALUE] = [0, 1, 2, 3, 4]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_forin_enum_cdef():
    """
    >>> test_carray_forin_enum_cdef()
    [0, 1, 2, 3, 4]
    """
    cdef int[INTERNAL_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    items = []
    for item in carray:  # cython.int
        items.append(item)
    return items


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_generator_enum_typing():
    """
    >>> list(test_carray_generator_enum_typing())
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[INTERNAL_ENUM_VALUE] = [0, 1, 2, 3, 4]

    for item in carray:  # cython.int
        yield item


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_generator_enum_cdef():
    """
    >>> list(test_carray_generator_enum_cdef())
    [0, 1, 2, 3, 4]
    """
    cdef int[INTERNAL_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    for item in carray:  # cython.int
        yield item


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_listcomp_enum_typing():
    """
    >>> test_carray_listcomp_enum_typing()
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[INTERNAL_ENUM_VALUE] = [0, 1, 2, 3, 4]

    return [item for item in carray]  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_listcomp_enum_cdef():
    """
    >>> test_carray_listcomp_enum_cdef()
    [0, 1, 2, 3, 4]
    """
    cdef int[INTERNAL_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    return [item for item in carray]  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_setcomp_enum_typing():
    """
    >>> sorted(test_carray_setcomp_enum_typing())
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[INTERNAL_ENUM_VALUE] = [0, 1, 2, 3, 4]

    return {item for item in carray}  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_setcomp_enum_cdef():
    """
    >>> sorted(test_carray_setcomp_enum_cdef())
    [0, 1, 2, 3, 4]
    """
    cdef int[INTERNAL_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    return {item for item in carray}  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_genexpr_enum_typing():
    """
    >>> list(test_carray_genexpr_enum_typing())
    [0, 1, 2, 3, 4]
    """
    carray: cython.int[INTERNAL_ENUM_VALUE] = [0, 1, 2, 3, 4]

    return (item for item in carray)  # cython.int


@cython.test_assert_path_exists("//CArrayNode")
def test_carray_genexpr_enum_cdef():
    """
    >>> list(test_carray_genexpr_enum_cdef())
    [0, 1, 2, 3, 4]
    """
    cdef int[INTERNAL_ENUM_VALUE] carray = [0, 1, 2, 3, 4]

    return (item for item in carray)  # cython.int
