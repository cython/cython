# mode: run
# tag: listcomp, comprehension

cimport cython


def smoketest():
    """
    >>> smoketest()
    [0, 4, 8]
    """
    x = 'abc'
    result = [x*2 for x in range(5) if x % 2 == 0]
    assert x != 'abc'
    return result


def list_genexp():
    """
    >>> list_genexp()
    [0, 4, 8]
    """
    x = 'abc'
    result = list(x*2 for x in range(5) if x % 2 == 0)
    assert x == 'abc'
    return result


def int_runvar():
    """
    >>> int_runvar()
    [0, 4, 8]
    """
    cdef int x
    print [x*2 for x in range(5) if x % 2 == 0]


cdef class A:
    def __repr__(self): return u"A"

def typed():
    """
    >>> typed()
    [A, A, A]
    """
    cdef A obj
    print [obj for obj in [A(), A(), A()]]


def inferred_type():
    """
    >>> inferred_type()
    ['A', 'A', 'A']
    """
    print [cython.typeof(obj) for obj in [A(), A(), A()]]


def not_inferred_type():
    """
    >>> not_inferred_type()
    ['Python object', 'Python object', 'Python object']
    """
    print [cython.typeof(obj) for obj in [1, A(), 'abc']]


def iterdict():
    """
    >>> iterdict()
    [1, 2, 3]
    """
    cdef dict d = dict(a=1,b=2,c=3)
    l = [d[key] for key in d]
    l.sort()
    print l


listcomp_result = [ i*i for i in range(5) ]
def global_listcomp():
    """
    >>> [ i*i for i in range(5) ]
    [0, 1, 4, 9, 16]
    >>> listcomp_result
    [0, 1, 4, 9, 16]
    """


class ListCompInClass(object):
    """
    >>> x = ListCompInClass()
    >>> x.listcomp
    [1, 2, 3]
    """
    listcomp = [i+1 for i in range(3)]


cdef class ListCompInCClass:
    """
    >>> x = ListCompInCClass()
    >>> x.listcomp
    [1, 2, 3]
    """
    listcomp = [i+1 for i in range(3)]


def nested_result():
    """
    >>> nested_result()
    [[], [-1], [-1, 0], [-1, 0, 1]]
    """
    result = [[a-1 for a in range(b)] for b in range(4)]
    return result


def listcomp_as_condition(sequence):
    """
    >>> listcomp_as_condition(['a', 'b', '+'])
    True
    >>> listcomp_as_condition('ab+')
    True
    >>> listcomp_as_condition('abc')
    False
    """
    if [1 for c in sequence if c in '+-*/<=>!%&|([^~,']:
        return True
    return False


@cython.test_fail_if_path_exists("//SimpleCallNode//ComprehensionNode")
@cython.test_assert_path_exists("//ComprehensionNode")
def sorted_listcomp(sequence):
    """
    >>> sorted_listcomp([])
    []
    >>> sorted_listcomp([1])
    [2]
    >>> sorted_listcomp([3,2,4])
    [3, 4, 5]
    """
    return sorted([ n+1 for n in sequence ])


@cython.test_fail_if_path_exists("//IfStatNode",
                                 "//ComprehensionAppendNode")
@cython.test_assert_path_exists("//ComprehensionNode")
def listcomp_const_condition_false():
    """
    >>> listcomp_const_condition_false()
    []
    """
    return [x*2 for x in range(3) if False]


@cython.test_fail_if_path_exists("//IfStatNode",
                                 "//ComprehensionAppendNode")
@cython.test_assert_path_exists("//ComprehensionNode")
def listcomp_const_condition_false_bool_test():
    """
    >>> listcomp_const_condition_false_bool_test()
    True
    """
    return not [l for l in [1] if False]


@cython.test_fail_if_path_exists("//IfStatNode",
                                 "//ComprehensionAppendNode")
@cython.test_assert_path_exists("//ComprehensionNode")
def listcomp_const_condition_false_assert():
    """
    >>> listcomp_const_condition_false_assert()
    """
    assert not [l for l in [1] if False]


@cython.test_fail_if_path_exists("//ComprehensionNode//IfStatNode",
                                 "//ComprehensionAppendNode")
@cython.test_assert_path_exists("//ComprehensionNode",
                                "//IfStatNode")
def listcomp_const_condition_false_if():
    """
    >>> listcomp_const_condition_false_if()
    True
    """
    if not [l for l in [1] if False]:
        return True
    return False


@cython.test_fail_if_path_exists("//ComprehensionNode//IfStatNode",
                                 "//ComprehensionAppendNode")
@cython.test_assert_path_exists("//ComprehensionNode",
                                "//IfStatNode")
def listcomp_const_condition_false_typed_error():
    """
    >>> listcomp_const_condition_false_typed_error()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    cdef str l
    if not [l for l in [1] if False]:
        return True
    return False


@cython.test_fail_if_path_exists("//IfStatNode")
@cython.test_assert_path_exists("//ComprehensionNode",
                                "//ComprehensionAppendNode")
def listcomp_const_condition_true():
    """
    >>> listcomp_const_condition_true()
    [0, 2, 4]
    """
    return [x*2 for x in range(3) if True]
