# cython: language_level=3
# mode: run
# tag: pure3.7, pep526, pep484, warnings

# for the benefit of the pure tests, don't require annotations
# to be evaluated
from __future__ import annotations
import cython

class A:
    pass


def test_generator_next_node_coercion(N: list[int]):
    """
    >>> test_generator_next_node_coercion([A()])  # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'A' and 'int'
    """
    return any(n < 0 for n in N)


def test_iterator_next_node_coercion(N: list[int]):
    """
    >>> test_iterator_next_node_coercion([A()])  # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'A' and 'int'
    """
    for n in N:
        if n < 0:
            return True
    return False


def test_assign_builtin_method():
    """
    >>> test_assign_builtin_method()
    int
    """
    l: list[list[cython.int]] = [[0]]
    i = l.pop().pop()
    print(cython.typeof(i))


def test_builtin_methods():
    """
    >>> test_builtin_methods()
    list:
    int 1
    set:
    str object a
    """
    print('list:')
    l: list[list[cython.int]] = [[1]]
    lp = l.pop().pop()
    print(cython.typeof(lp), lp)

    print('set:')
    s: set[str] = {'a'}
    sg = s.pop()
    print(cython.typeof(sg) + (' object' if not cython.compiled else ''), sg)

def test_dict_handle_none():
    """
    >>> test_dict_handle_none()
    str object
    str object
    """

    none_dict: dict[str, str] = {'none': None}
    # get() with None value
    assert 'none' in none_dict
    none_value = none_dict.get('none')
    print(cython.typeof(none_value) if cython.compiled else 'str object')
    try:
        len(none_value)
    except TypeError:
        pass
    else:
        assert False, len(none_value)
    # pop() with None value
    assert 'none' in none_dict
    popped_value = none_dict.pop('none')
    print(cython.typeof(popped_value) if cython.compiled else 'str object')
    try:
        len(popped_value)
    except TypeError:
        pass
    else:
        assert False, len(none_value)

def test_dict_handle_missing_key():
    """
    >>> test_dict_handle_missing_key()
    * get():
    str object
    str object
    str object
    Python object
    * pop():
    str object
    Python object
    * setdefault():
    str object
    str object
    """

    empty_dict: dict[str, str] = {}
    print("* get():")

    # get() with missing key
    missing = empty_dict.get('missing')
    print(cython.typeof(missing) if cython.compiled else 'str object')
    try:
        len(missing)
    except TypeError:
        pass
    else:
        assert False, len(missing)
    # get() with missing key and default as None
    missing_none = empty_dict.get('missing', None)
    print(cython.typeof(missing_none) if cython.compiled else 'str object')
    try:
        len(missing_none)
    except TypeError:
        pass
    else:
        assert False, len(missing_none)
    # get() with missing key and default as string
    missing_default = empty_dict.get('missing', 'value')
    print(cython.typeof(missing_default) + (' object' if not cython.compiled else ''))
    assert len(missing_default) == len('value'), len(missing_default)
    assert missing_default == 'value', missing_default
    # get() with missing key and default as None
    popped_missing = empty_dict.pop('missing', None)
    try:
        len(popped_missing)
    except TypeError:
        pass
    else:
        assert False, len(popped_missing)
    # get() with missing key and default as None without assignment
    print(cython.typeof(empty_dict.get('missing')) if cython.compiled else 'Python object')

    print("* pop():")
    # pop() with missing key and default as string
    popped_default = empty_dict.pop('missing', 'value')
    print(cython.typeof(popped_default) + (' object' if not cython.compiled else ''))
    assert len(popped_default) == len('value'), len(popped_default)
    assert popped_default == 'value', popped_default
    # pop() with missing key and default as int
    popped_int = empty_dict.pop('missing', 5)
    print(cython.typeof(popped_int) if cython.compiled else 'Python object')

    print("* setdefault():")
    # setdefault() with missing key and default as string
    assert 'missing' not in empty_dict
    inserted_default = empty_dict.setdefault('missing', 'value')
    print(cython.typeof(inserted_default) if cython.compiled else 'str object')
    assert inserted_default == 'value', inserted_default
    assert empty_dict['missing'] == 'value', empty_dict
    # setdefault() with missing key
    assert 'none_missing' not in empty_dict
    inserted_default_none = empty_dict.setdefault('none_missing')
    print(cython.typeof(inserted_default_none) if cython.compiled else 'str object')
    try:
        len(inserted_default_none)
    except TypeError:
        pass
    else:
        assert False, len(inserted_default_none)
    assert inserted_default_none is None, inserted_default_none
    assert empty_dict['none_missing'] is None, empty_dict

def test_dict_builtin_methods():
    """
    >>> test_dict_builtin_methods()
    get:
    int object 2
    popitem:
    tuple[str object,int object] object ('a', 2)
    keys:
    dict_keys[str object] object
    str object a
    values:
    dict_values[int object] object
    int object 2
    items:
    dict_items[tuple[str object,int object] object] object
    tuple[str object,int object] object ('a', 2)
    """
    d: dict[str, int] = {'a': 2}

    print("get:")
    dg = d.get('a')
    print(cython.typeof(dg) + (' object' if not cython.compiled else ''), dg)

    print("popitem:")
    dpi = d.popitem()
    if cython.compiled:
        print(cython.typeof(dpi), dpi)
    else:
        print("tuple[str object,int object] object ('a', 2)")

    d = {'a': 2}

    print("keys:")
    dk = d.keys()
    print(cython.typeof(dk)+ ('[str object] object' if not cython.compiled else ''))
    for i in dk:
        print(cython.typeof(i) + (' object' if not cython.compiled else ''), i)

    print("values:")
    dv = d.values()
    print(cython.typeof(dv) + ('[int object] object' if not cython.compiled else ''))
    for j in dv:
        print(cython.typeof(j) + (' object' if not cython.compiled else ''), j)

    print("items:")
    di = d.items()
    print(cython.typeof(di) + ('[tuple[str object,int object] object] object' if not cython.compiled else ''))
    for k in di:
        print(cython.typeof(k) + ('[str object,int object] object' if not cython.compiled else ''), k)
