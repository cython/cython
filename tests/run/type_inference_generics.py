# cython: language_level=3
# mode: run
# tag: pure3.7, pep526, pep484, warnings

# for the benefit of the pure tests, don't require annotations
# to be evaluated
from __future__ import annotations
import cython
import sys

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


def new_object():
    return object()

def test_initialised_subscripted_frozenset(arg_a: list[int], arg_b):
    """
    >>> test_initialised_subscripted_frozenset([], [])
    * simple frozenset:
    frozenset[long] object long
    frozenset object
    frozenset object Python object
    frozenset object Python object
    frozenset object Python object
    * frozenset from function:
    frozenset[Py_ssize_t] object
    frozenset object
    * frozenset from variable:
    frozenset[int object] object
    frozenset object
    * nested container:
    frozenset[(long, long)] object tuple object
    frozenset[(long, long)] object tuple object
    """
    print("* simple frozenset:")
    s1 = frozenset({1})
    for i1 in s1:
        print(
            cython.typeof(s1) + ('[long] object' if not cython.compiled else ''),
            'long' if not cython.compiled else cython.typeof(i1)
        )
    s2 = frozenset()
    print(cython.typeof(s2) + (' object' if not cython.compiled else ''))

    s3 = frozenset({1, 3.0, "5"})
    for i3 in s3:
        print(
            cython.typeof(s3) + (' object' if not cython.compiled else ''),
            cython.typeof(i3) if cython.compiled else "Python object"
        )

    print("* frozenset from function:")
    s4 = frozenset({len(s3)})
    print(cython.typeof(s4) + ('[Py_ssize_t] object' if not cython.compiled else ''))

    s5 = frozenset({new_object()})
    print(cython.typeof(s5) + (' object' if not cython.compiled else ''))

    print("* frozenset from variable:")
    s6 = frozenset(arg_a)
    print(cython.typeof(s6) + ('[int object] object' if not cython.compiled else ''))

    s7 = frozenset(arg_b)
    print(cython.typeof(s7) + (' object' if not cython.compiled else ''))

    print("* nested container:")
    s8 = frozenset({(1, 2), (3, 4)})
    for i8 in s8:
        print(
            cython.typeof(s8) + ('[(long, long)] object' if not cython.compiled else ''),
            cython.typeof(i8) + (' object' if not cython.compiled else '')
    )

def test_infer_frozenset_from_list():
    """
    >>> test_infer_frozenset_from_list()
    frozenset[long] object
    frozenset object
    """
    s1 = frozenset([1, 2, 3])
    print(cython.typeof(s1) + ('[long] object' if not cython.compiled else ''))
    s2 = frozenset([1, "a"])
    print(cython.typeof(s2) + (' object' if not cython.compiled else ''))

def test_infer_frozenset_from_tuple():
    """
    >>> test_infer_frozenset_from_tuple()
    frozenset[long] object
    frozenset[Python object] object
    """
    s1 = frozenset((1, 2, 3))
    print(cython.typeof(s1) + ('[long] object' if not cython.compiled else ''))
    s2 = frozenset((1, "a"))
    print(cython.typeof(s2) + ('[Python object] object' if not cython.compiled else ''))


def test_infer_frozenset_from_dict():
    """
    >>> test_infer_frozenset_from_dict()
    frozenset[long] object
    frozenset[Python object] object
    """
    s1 = frozenset({1: 'a', 2: 'b', 3: 'c'})
    print(cython.typeof(s1) + ('[long] object' if not cython.compiled else ''))
    s2 = frozenset({'a': 'a', 2: 'b', 3: 'c'})
    print(cython.typeof(s2) + ('[Python object] object' if not cython.compiled else ''))

if sys.version_info >= (3, 15) or cython.compiled:

    def test_initialised_subscripted_frozendict(arg_a: dict[str,int], arg_b):
        """
        >>> test_initialised_subscripted_frozendict({}, {})
        * basic frozendict:
        frozendict[long,str object] object long
        frozendict object
        * non-uniform keys and values:
        frozendict[Python object,long] object Python object
        frozendict[Python object,long] object Python object
        frozendict[Python object,long] object Python object
        frozendict[long,Python object] object long
        frozendict[long,Python object] object long
        frozendict[long,Python object] object long
        * len() function:
        frozendict[Py_ssize_t,str object] object
        frozendict[str object,Py_ssize_t] object
        * not annotated function:
        frozendict[Python object,long] object
        frozendict[long,Python object] object
        * frozendict created from variable:
        frozendict[str object,int object] object
        frozendict object
        * recursive containers:
        frozendict[long,list object] object list object
        frozendict[long,tuple[str object,str object] object] object tuple[str object,str object] object
        frozendict[long,Python object] object Python object
        frozendict[Python object,str object] object str object
        """
        print("* basic frozendict:")
        s1 = frozendict({1: 'a'})
        for i1 in s1:
            print(
                cython.typeof(s1) + ('[long,str object] object' if not cython.compiled else ''),
                'long' if not cython.compiled else cython.typeof(i1)
            )
        s2 = frozendict()
        print(cython.typeof(s2) + (' object' if not cython.compiled else ''))

        print("* non-uniform keys and values:")
        s3 = frozendict({1: 1, 3.0: 2, "5": 3})
        for i3 in s3:
            print(
                cython.typeof(s3) + ('[Python object,long] object' if not cython.compiled else ''),
                'Python object' if not cython.compiled else cython.typeof(i3)
            )
        s4 = frozendict({1: 1, 2: 3.0, 3: "5"})
        for i4 in s4:
            print(
                cython.typeof(s4) + ('[long,Python object] object' if not cython.compiled else ''),
                'long' if not cython.compiled else cython.typeof(i4)
            )

        print("* len() function:")
        s5 = frozendict({len(s3): 'a'})
        print(cython.typeof(s5) + ('[Py_ssize_t,str object] object' if not cython.compiled else ''))
        s6 = frozendict({'a': len(s3)})
        print(cython.typeof(s6) + ('[str object,Py_ssize_t] object' if not cython.compiled else ''))

        print("* not annotated function:")
        s7 = frozendict({new_object(): 1})
        print(cython.typeof(s7) + ('[Python object,long] object' if not cython.compiled else ''))
        s8 = frozendict({1: new_object()})
        print(cython.typeof(s8) + ('[long,Python object] object' if not cython.compiled else ''))

        print("* frozendict created from variable:")
        s9 = frozendict(arg_a)
        print(cython.typeof(s9) + ('[str object,int object] object' if not cython.compiled else ''))
        s10 = frozendict(arg_b)
        print(cython.typeof(s10) + (' object' if not cython.compiled else ''))

        print("* recursive containers:")
        s11 = frozendict({1: ['a', 'b']})  # mutable containers should not have inferred subscripts
        print(
            cython.typeof(s11) + ('[long,list object] object' if not cython.compiled else ''),
            cython.typeof(s11[1]) + (' object' if not cython.compiled else '')
        )
        s12 = frozendict({1: ('a', 'b'), 2: ('a', 'b')})  # consistent tuples should have inferred subscripts
        print(
            cython.typeof(s12) + ('[long,tuple[str object,str object] object] object' if not cython.compiled else ''),
            cython.typeof(s12[1]) + ('[str object,str object] object' if not cython.compiled else '')
        )
        s13 = frozendict({1: ('a', 'b'), 2: ('a', 'b', 'c')})  # in-consistent tuples should not have inferred subscripts
        print(
            cython.typeof(s13) + ('[long,Python object] object' if not cython.compiled else ''),
            'Python object' if not cython.compiled else cython.typeof(s13[2])
        )
        s14 = frozendict({(1, 2): 'a', ('a', 'b'): 'c'})  # in-consistent tuples should not have inferred subscripts
        print(
            cython.typeof(s14) + ('[Python object,str object] object' if not cython.compiled else ''),
            cython.typeof(s14[(1, 2)]) + (' object' if not cython.compiled else '')
        )


def test_initialised_subscripted_mutables_types():
    """
    >>> test_initialised_subscripted_mutables_types()
    list object list object
    set object set object
    dict object dict object
    """
    l1 = [1, 3, 5]
    l2 = list([1, 3, 5])
    print(
        cython.typeof(l1) + (' object' if not cython.compiled else ''),
        cython.typeof(l2) + (' object' if not cython.compiled else '')
    )
    s1 = {1, 3, 5}
    s2 = set({1, 3, 5})
    print(
        cython.typeof(s1) + (' object' if not cython.compiled else ''),
        cython.typeof(s2) + (' object' if not cython.compiled else '')
    )
    d1 = {1: 1, 3: 2, 5: 3}
    d2 = dict({1: 1, 3: 2, 5: 3})
    print(
        cython.typeof(d1) + (' object' if not cython.compiled else ''),
        cython.typeof(d2) + (' object' if not cython.compiled else '')
    )

def append_one(t) -> tuple:
    return tuple(t) + (1,)

@cython.cfunc
def c_append_one(t) -> tuple:
    return tuple(t) + (1,)

def inferred():
    x = append_one(['a', 'b'])

def test_initialized_custom_function_not_inferred():
    """
    >>> test_initialized_custom_function_not_inferred()
    Python object
    tuple object
    tuple[str object,...] object
    """
    # Tests that regular functions does not infer subscripted types
    x = append_one(['a', 'b'])
    y = c_append_one(['a', 'b'])
    z = tuple(['a', 'b'])
    print(cython.typeof(x) if cython.compiled else 'Python object')
    print(cython.typeof(y) + (' object' if not cython.compiled else ''))
    print(cython.typeof(z) + ('[str object,...] object' if not cython.compiled else ''))

def test_initialised_tuple(arg_l: list[str]):
    """
    >>> test_initialised_tuple(['bar'])
    * simple tuple
    tuple object
    tuple[long,long,str object] object
    tuple object
    tuple[str object,str object] object
    * tuple constructed from variable
    tuple object
    tuple[long,long,str object] object
    tuple[str object,...] object
    * tuple containing containers
    tuple[long,str object,list object] object
    tuple[long,str object,(long, long, long)] object
    """
    print("* simple tuple")
    t1 = (1, 2, 3)
    print(cython.typeof(t1) + (' object' if not cython.compiled else ''))
    t2 = (1, 2, 'bar')
    print(cython.typeof(t2) + ('[long,long,str object] object' if not cython.compiled else ''))
    t3 = ()
    print(cython.typeof(t3) + (' object' if not cython.compiled else ''))
    t4 = tuple(("bar", "foo"))
    print(cython.typeof(t4) + ('[str object,str object] object' if not cython.compiled else ''))

    print("* tuple constructed from variable")
    t5 = tuple(t1)
    print(cython.typeof(t5) + (' object' if not cython.compiled else ''))
    t6 = tuple(t2)
    print(cython.typeof(t6) + ('[long,long,str object] object' if not cython.compiled else ''))
    t7 = tuple(arg_l)
    print(cython.typeof(t7) + ('[str object,...] object' if not cython.compiled else ''))

    print("* tuple containing containers")
    t8 = (1, "bar", [1, 2, 3])
    # mutable containers must not have inferred subscripted types
    print(cython.typeof(t8) + ('[long,str object,list object] object' if not cython.compiled else ''))
    t9 = (1, "bar", (1, 2, 3))
    print(cython.typeof(t9) + ('[long,str object,(long, long, long)] object' if not cython.compiled else ''))
