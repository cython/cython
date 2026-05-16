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
    tuple object
    tuple object
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


def bar():
    return object()


def test_initialised_subscripted_set():
    """
    >>> test_initialised_subscripted_set()
    Testing set[int]:
    ('set[int object] object', 'int object')
    ('set[int object] object', 'int object')
    ('set[int object] object', 'int object')
    Testing set:
    set object
    Testing set with mixed types:
    ('set object', 'Python object')
    ('set object', 'Python object')
    ('set object', 'Python object')
    Testing set with inferable function call:
    set[int object] object
    Testing set with noninferrable function call:
    set object
    """
    print("Testing set[int]:")
    s1 = {1, 3, 5}
    for i1 in s1:
        print(cython.typeof(s1), cython.typeof(i1))
    print("Testing set:")
    s2 = set()
    print(cython.typeof(s2))
    print("Testing set with mixed types:")
    s3 = {1, 3.0, "5"}
    for i3 in s3:
        print(cython.typeof(s3), cython.typeof(i3))
    print("Testing set with inferable function call:")
    s4 = {len(s3)}
    print(cython.typeof(s4))
    print("Testing set with noninferrable function call:")
    s5 = {bar()}
    print(cython.typeof(s5))


def test_initialised_subscripted_list():
    """
    >>> test_initialised_subscripted_list()
    Testing list[int]:
    (1, 'list[int object] object', 'int object')
    (3, 'list[int object] object', 'int object')
    (5, 'list[int object] object', 'int object')
    [1, 0, 5]
    Testing list:
    list object
    Testing list with mixed types:
    (1, 'list object', 'Python object')
    (3.0, 'list object', 'Python object')
    ('5', 'list object', 'Python object')
    [1, 0, '5']
    Testing list with inferable function call:
    list[int object] object
    Testing list with noninferrable function call:
    list object
    """
    print("Testing list[int]:")
    l1 = [1, 3, 5]
    for i1 in l1:
        print(i1, cython.typeof(l1), cython.typeof(i1))
    l1[1] = 0
    print(l1)
    print("Testing list:")
    l2 = []
    print(cython.typeof(l2))
    print("Testing list with mixed types:")
    l3 = [1, 3.0, "5"]
    for i3 in l3:
        print(i3, cython.typeof(l3), cython.typeof(i3))
    l3[1] = 0
    print(l3)
    print("Testing list with inferable function call:")
    l4 = [len(l3)]
    print(cython.typeof(l4))
    print("Testing list with noninferrable function call:")
    l5 = [bar()]
    print(cython.typeof(l5))


def test_initialised_subscripted_dict():
    """
    >>> test_initialised_subscripted_dict()
    Testing dict[int, str]:
    ('dict[int object,str object] object', 'int object', 'str object')
    ('dict[int object,str object] object', 'int object', 'str object')
    ('dict[int object,str object] object', 'int object', 'str object')
    Testing dict:
    dict object
    Testing dict with mixed key types:
    ('dict[Python object,int object] object', 'Python object', 'int object')
    ('dict[Python object,int object] object', 'Python object', 'int object')
    ('dict[Python object,int object] object', 'Python object', 'int object')
    Testing dict with mixed value types:
    ('dict[int object,Python object] object', 'int object', 'Python object')
    ('dict[int object,Python object] object', 'int object', 'Python object')
    ('dict[int object,Python object] object', 'int object', 'Python object')
    Testing dict with mixed key and value types:
    ('dict object', 'Python object', 'Python object')
    ('dict object', 'Python object', 'Python object')
    ('dict object', 'Python object', 'Python object')
    Testing dict with inferable function call:
    dict[int object,int object] object
    Testing dict with noninferrable function call:
    dict object
    """
    print("Testing dict[int, str]:")
    d1 = {1: "a", 3: "b", 5: "c"}
    for k1 in d1:
        print(cython.typeof(d1), cython.typeof(k1), cython.typeof(d1[k1]))

    print("Testing dict:")
    d2 = {}
    print(cython.typeof(d2))

    print("Testing dict with mixed key types:")
    d3 = {1: 1, 3.0: 3, "5": 5}
    for k3 in d3:
        print(cython.typeof(d3), cython.typeof(k3), cython.typeof(d3[k3]))

    print("Testing dict with mixed value types:")
    d4 = {1: 1.0, 3: "b", 5: "c"}
    for k4 in d4:
        print(cython.typeof(d4), cython.typeof(k4), cython.typeof(d4[k4]))

    print("Testing dict with mixed key and value types:")
    d5 = {1: 1.0, 3.0: "b", "5": "c"}
    for k5 in d5:
        print(cython.typeof(d5), cython.typeof(k5), cython.typeof(d5[k5]))

    print("Testing dict with inferable function call:")
    d6 = {len(d1): len(d2), len(d3): len(d5)}
    print(cython.typeof(d6))

    print("Testing dict with noninferrable function call:")
    d7 = {bar(): bar()}
    print(cython.typeof(d7))


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

