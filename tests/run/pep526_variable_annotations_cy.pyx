# mode: run

import cython

try:
    import typing
    from typing import List, Tuple
    from typing import Set as _SET_
except:
    pass  # this should allow Cython to interpret the directives even when the module doesn't exist

def test_subscripted_types():
    """
    >>> test_subscripted_types()
    dict[int,float] object
    list[int] object
    set[Python object] object
    """
    cdef typing.Dict[int, float] a = {}
    cdef List[int] b = []
    cdef _SET_[object] c = set()

    print(cython.typeof(a))
    print(cython.typeof(b))
    print(cython.typeof(c))


def test_casting_subscripted_types():
    """
    >>> test_casting_subscripted_types()
    Lists:
    list[int] object
    1
    list object
    1.0
    Dicts:
    dict[str object,float] object
    2.0
    dict object
    2
    float
    3.0
    Python object
    3
    """
    print("Lists:")
    cdef list[float] l = [1.0, 2.0]
    print(cython.typeof((<list[int]> l)))
    print((<list[int]> l)[0])

    print(cython.typeof((<list> l)))
    print((<list> l)[0])
    print("Dicts:")
    cdef dict[str, int] d = {'a': 1, 'b': 2}
    print(
        cython.typeof((<dict[str, float]> d)))
    print((<dict[str, float]> d)['b'])
    print(cython.typeof((<dict> d)))
    print((<dict> d)['b'])

    cdef dict[int, str] d2 = {3: '3'}
    for k1 in <dict[float, str]> d2:
        print(cython.typeof(k1))
        print(k1)

    for k2 in <dict> d2:
        print(cython.typeof(k2))
        print(k2)


cdef class TestClassVar:
    """
    >>> TestClassVar.cls
    5
    >>> TestClassVar.regular  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    AttributeError:
    """
    cdef int regular
    cdef typing.ClassVar[int] cls
    cls = 5

# because tuple is specifically special cased to go to ctuple where possible
def test_tuple(typing.Tuple[int, float] a,  typing.Tuple[int, ...] b,
               Tuple[int, object] c  # cannot be a ctuple
               ):
    """
    >>> test_tuple((1, 1.0), (1, 1.0), (1, 1.0))
    int
    int
    tuple[int,...] object
    tuple[int,Python object] object
    """
    cdef typing.Tuple[int, float] x = (a[0], a[1])  # C int/float
    cdef Tuple[int, ...] y = (1,2.)
    z = a[0]  # should infer to C int

    print(cython.typeof(z))
    print(cython.typeof(x[0]))
    print(cython.typeof(y))
    print(cython.typeof(c))

def test_tuple_assignment(i, list[int] la, set[int] sa, dict[int, int] da, frozenset[int] fa):
    """
    >>> test_tuple_assignment(0, [], set(), {}, frozenset({}))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:
    >>> test_tuple_assignment(1, [], set(), {}, frozenset({}))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:
    >>> test_tuple_assignment(2, [], set(), {}, frozenset({}))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:
    >>> test_tuple_assignment(3, [], set(), {}, frozenset({}))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:
    """
    cdef tuple[int] ta = (1,)
    if i == 0:
        la = ta
    elif i == 1:
        sa = ta
    elif i == 2:
        da = ta
    elif i == 3:
        fa = ta


def test_nested_tuple():
    """
    >>> test_nested_tuple()
    tuple[dict[tuple[str object,int] object,tuple[int,str object] object] object,list[(int, int)] object,set[(float, float)] object,tuple[tuple[str object,int] object,tuple[int,str object] object] object] object
    ta[0]:
    dict[tuple[str object,int] object,tuple[int,str object] object] object
    tuple[int,str object] object
    ta[1]:
    list[(int, int)] object
    (int, int)
    ta[2]:
    set[(float, float)] object
    ta[3]:
    tuple[tuple[str object,int] object,tuple[int,str object] object] object
    tuple[str object,int] object
    tuple[int,str object] object
    str object
    int
    int
    str object
    """
    cdef tuple[
        dict[tuple[str, int], tuple[int, str]],
        list[tuple[int, int]],
        set[tuple[float, float]],
        tuple[tuple[str, int], tuple[int, str]]
    ] ta = (
        {('a', 1): (2, 'b')},
        [(1, 2), (3, 4)],
        {(1.0, 2.0), (3.0, 4.0)}
    )
    print(cython.typeof(ta))
    print('ta[0]:')
    print(cython.typeof(ta[0]))
    print(cython.typeof(ta[0][('a', 1)]))
    print('ta[1]:')
    print(cython.typeof(ta[1]))
    print(cython.typeof(ta[1][1]))
    print('ta[2]:')
    print(cython.typeof(ta[2]))
    print('ta[3]:')
    print(cython.typeof(ta[3]))
    print(cython.typeof(ta[3][0]))
    print(cython.typeof(ta[3][1]))
    print(cython.typeof(ta[3][0][0]))
    print(cython.typeof(ta[3][0][1]))
    print(cython.typeof(ta[3][1][0]))
    print(cython.typeof(ta[3][1][1]))


def test_nested_list():
    """
    >>> test_nested_list()
    list[list[int] object] object
    list[int] object
    int
    1
    """
    cdef list[list[int]] la = [[1]]
    print(cython.typeof(la))
    print(cython.typeof(la[0]))
    print(cython.typeof(la[0][0]))
    print(la[0][0])

def test_nested_set():
    """
    >>> test_nested_set()
    set[frozenset[int] object] object
    frozenset[int] object
    int
    1
    """
    cdef set[frozenset[int]] sa = {frozenset({1})}
    print(cython.typeof(sa))
    for fs in sa:
        print(cython.typeof(fs))
        for s in fs:
            print(cython.typeof(s))
            print(s)

def test_nested_dict():
    """
    >>> test_nested_dict()
    dict[frozenset[str object] object,list[int] object] object
    frozenset[str object] object
    list[int] object
    int
    2
    str object
    a
    """
    cdef dict[frozenset[str], list[int]] da = {frozenset({"a"}): [2]}
    print(cython.typeof(da))
    for dk in da:
        print(cython.typeof(dk))
        print(cython.typeof(da[dk]))
        for l in da[dk]:
            print(cython.typeof(l))
            print(l)
        for fs in dk:
            print(cython.typeof(fs))
            print(fs)

def test_nested_frozenset():
    """
    >>> test_nested_frozenset()
    frozenset[frozenset[int] object] object
    frozenset[int] object
    int
    1
    """
    fa: frozenset[frozenset[cython.int]] = frozenset({frozenset({1})})
    print(cython.typeof(fa))
    for f in fa:
        print(cython.typeof(f))
        for a in f:
            print(cython.typeof(a))
            print(a)

def common_container_type(cond, list[float] a, list[int] b):
    """
    >>> common_container_type(True, [1.0], [2])
    ([1.0], 'list object')
    >>> common_container_type(False, [1.0], [2])
    ([2], 'list object')
    """
    result = a if cond else b
    print(result, cython.typeof(result))

cdef class MyClass:
    pass

def test_list_of_extensions(myclass):
    """
    >>> test_list_of_extensions(MyClass())  # doctest: +ELLIPSIS
    list[MyClass] object
    MyClass
    <pep526_variable_annotations_cy.MyClass object at ...>
    >>> test_list_of_extensions(5)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:
    """
    cdef list[MyClass] l = [MyClass()]
    l[0] = myclass
    print(cython.typeof(l))
    print(cython.typeof(l[0]))
    print(l[0])

def test_dict_of_extensions(myclass):
    """
    >>> test_dict_of_extensions(MyClass())  # doctest: +ELLIPSIS
    dict[int,MyClass] object
    MyClass
    <pep526_variable_annotations_cy.MyClass object at ...>
    >>> test_dict_of_extensions(5)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:
    """
    cdef dict[int, MyClass] l = {0: MyClass()}
    l[0] = myclass
    print(cython.typeof(l))
    print(cython.typeof(l[0]))
    print(l[0])


def test_list_slice():
    """
    >>> test_list_slice()
    list[int] object
    int
    """
    cdef list[int] l = [1, 2, 3]
    print(cython.typeof(l[::-1]))
    print(cython.typeof(l[::-1][0]))


def test_tuple_with_not_constant_index(tuple[str, int] a, int index):
    """
    >>> test_tuple_with_not_constant_index(("Foo", 1), 0)
    ('Python object', 'Foo')
    >>> test_tuple_with_not_constant_index(("Foo", 1), 1)
    ('Python object', 1)
    >>> test_tuple_with_not_constant_index(("Foo", 1), "not an int")   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: an integer is required
    """
    print(cython.typeof(a[index]), a[index])
