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


def bar():
    return object()


def test_initialised_subscripted_frozenset(a: list[int], b):
    """
    >>> test_initialised_subscripted_frozenset([], [])
    ('frozenset[int object] object', 'int object')
    frozenset object
    ('frozenset object', 'Python object')
    ('frozenset object', 'Python object')
    ('frozenset object', 'Python object')
    frozenset[int object] object
    frozenset object
    frozenset[int object] object
    frozenset object
    """
    # TODO: Test nested types like frozenset({(1, 2)})
    s1 = frozenset({1})
    for i1 in s1:
        print(cython.typeof(s1), cython.typeof(i1))

    s2 = frozenset()
    print(cython.typeof(s2))

    s3 = frozenset({1, 3.0, "5"})
    for i3 in s3:
        print(cython.typeof(s3), cython.typeof(i3))

    s4 = frozenset({len(s3)})
    print(cython.typeof(s4))

    s5 = frozenset({bar()})
    print(cython.typeof(s5))

    s6 = frozenset(a)
    print(cython.typeof(s6))

    s7 = frozenset(b)
    print(cython.typeof(s7))


def test_initialised_subscripted_frozendict(a: dict[str,int], b):
    """
    >>> test_initialised_subscripted_frozendict({}, {})
    ('frozendict[int object,str object] object', 'int object')
    frozendict object
    ('frozendict[Python object,int object] object', 'Python object')
    ('frozendict[Python object,int object] object', 'Python object')
    ('frozendict[Python object,int object] object', 'Python object')
    ('frozendict[int object,Python object] object', 'int object')
    ('frozendict[int object,Python object] object', 'int object')
    ('frozendict[int object,Python object] object', 'int object')
    frozendict[int object,str object] object
    frozendict[str object,int object] object
    frozendict[Python object,int object] object
    frozendict[int object,Python object] object
    frozendict[str object,int object] object
    frozendict object
    """
    # TODO: Test nested types like frozendict({1: ['a', 'b']})
    s1 = frozendict({1: 'a'})
    for i1 in s1:
        print(cython.typeof(s1), cython.typeof(i1))

    s2 = frozendict()
    print(cython.typeof(s2))

    s3 = frozendict({1: 1, 3.0: 2, "5": 3})
    for i3 in s3:
        print(cython.typeof(s3), cython.typeof(i3))

    s4 = frozendict({1: 1, 2: 3.0, 3: "5"})
    for i4 in s4:
        print(cython.typeof(s4), cython.typeof(i4))

    s5 = frozendict({len(s3): 'a'})
    print(cython.typeof(s5))

    s6 = frozendict({'a': len(s3)})
    print(cython.typeof(s6))

    s7 = frozendict({bar(): 1})
    print(cython.typeof(s7))

    s8 = frozendict({1: bar()})
    print(cython.typeof(s8))

    s9 = frozendict(a)
    print(cython.typeof(s9))

    s10 = frozendict(b)
    print(cython.typeof(s10))


def test_initialised_subscripted_mutables_types():
    """
    >>> test_initialised_subscripted_mutables_types()
    ('list object', 'list object')
    ('set object', 'set object')
    ('dict object', 'dict object')
    """
    l1 = [1, 3, 5]
    l2 = list([1, 3, 5])
    print(cython.typeof(l1), cython.typeof(l2))
    s1 = {1, 3, 5}
    s2 = set({1, 3, 5})
    print(cython.typeof(s1), cython.typeof(s2))
    d1 = {1: 1, 3: 2, 5: 3}
    d2 = dict({1: 1, 3: 2, 5: 3})
    print(cython.typeof(d1), cython.typeof(d2))


def test_initialised_tuple(l: list[str]):
    """
    >>> test_initialised_tuple(['bar'])
    tuple object
    tuple[long,long,str object] object
    tuple object
    tuple object
    tuple[long,long,str object] object
    tuple[str object,...] object
    tuple[str object,str object] object
    """
    t1 = (1, 2, 3)
    print(cython.typeof(t1))
    t2 = (1, 2, 'bar')
    print(cython.typeof(t2))
    t3 = ()
    print(cython.typeof(t3))
    t4 = tuple(t1)
    print(cython.typeof(t4))
    t5 = tuple(t2)
    print(cython.typeof(t5))
    t6 = tuple(l)
    print(cython.typeof(t6))
    t7 = tuple(("bar", "foo"))
    print(cython.typeof(t7))
