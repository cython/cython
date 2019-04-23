# cython: language_level=3, binding=True
# mode: run
# tag: generators, python3, exceptions

print(end='')  # test that language_level 3 applies immediately at the module start, for the first token.

cimport cython

__doc__ = """
>>> items = sorted(locals_function(1).items())
>>> for item in items:
...     print('%s = %r' % item)
a = 1
b = 2
x = u'abc'

>>> except_as_deletes
True
>>> no_match_does_not_touch_target
True
"""

import sys
IS_PY2 = sys.version_info[0] < 3
if not IS_PY2:
    __doc__ = __doc__.replace(" u'", " '")

def locals_function(a, b=2):
    x = 'abc'
    return locals()


### true division

def truediv(x):
    """
    >>> truediv(4)
    2.0
    >>> truediv(3)
    1.5
    """
    return x / 2


def truediv_int(int x):
    """
    >>> truediv_int(4)
    2.0
    >>> truediv_int(3)
    1.5
    """
    return x / 2


@cython.cdivision(True)
def cdiv_int(int x):
    """
    >>> cdiv_int(4)
    2
    >>> cdiv_int(3)
    1
    """
    return x / 2


### module level except-as tests

exc = [None]
e = None
try:
    raise KeyError
except AttributeError as e:
    exc[0] = e
except KeyError       as e:
    exc[0] = e
except IndexError     as e:
    exc[0] = e
except:
    exc[0] = 'SOMETHING ELSE'

try:
    e
except NameError:
    except_as_deletes = True
else:
    except_as_deletes = False


e = 123
try:
    raise TypeError
except NameError as e:
    pass
except TypeError:
    pass
no_match_does_not_touch_target = (e == 123)


### more except-as tests

def except_as_no_raise_does_not_touch_target(a):
    """
    >>> except_as_no_raise_does_not_touch_target(TypeError)
    (1, 1)
    """
    d = a  # mark used

    b = 1
    try:
        i = 1
    except a as b:
        i = 2
    return i, b


def except_as_raise_deletes_target(x, a):
    """
    >>> except_as_raise_deletes_target(None, TypeError)
    1
    1
    >>> except_as_raise_deletes_target(TypeError('test'), TypeError)
    Traceback (most recent call last):
    UnboundLocalError: local variable 'b' referenced before assignment
    >>> except_as_raise_deletes_target(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> except_as_raise_deletes_target(None, TypeError)
    1
    1
    """
    b = 1
    try:
        i = 1
        if x:
            raise x
    except a as b:
        i = 2
        assert isinstance(b, a)
    print(b)  # raises UnboundLocalError if except clause was executed
    return i


def except_as_raise_deletes_target_even_after_del(x, a):
    """
    >>> except_as_raise_deletes_target_even_after_del(None, TypeError)
    1
    1
    >>> except_as_raise_deletes_target_even_after_del(TypeError('test'), TypeError)
    2
    >>> except_as_raise_deletes_target_even_after_del(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> except_as_raise_deletes_target_even_after_del(None, TypeError)
    1
    1
    """
    b = 1
    try:
        i = 1
        if x:
            raise x
    except a as b:
        i = 2
        assert isinstance(b, a)
        del b  # let's see if Cython can still 'del' it after this line!
    try:
        print(b)  # raises UnboundLocalError if except clause was executed
    except UnboundLocalError:
        pass
    else:
        if x:
            print("UnboundLocalError not raised!")
    return i


def except_as_raise_deletes_target_on_error(x, a):
    """
    >>> except_as_raise_deletes_target_on_error(None, TypeError)
    1
    1
    >>> except_as_raise_deletes_target_on_error(TypeError('test'), TypeError)
    Traceback (most recent call last):
    UnboundLocalError: local variable 'b' referenced before assignment
    >>> except_as_raise_deletes_target_on_error(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> except_as_raise_deletes_target_on_error(None, TypeError)
    1
    1
    """
    b = 1
    try:
        try:
            i = 1
            if x:
                raise x
        except a as b:
            i = 2
            raise IndexError("TEST")
    except IndexError as e:
        assert 'TEST' in str(e), str(e)
    print(b)  # raises UnboundLocalError if except clause was executed
    return i


def except_as_raise_with_empty_except(x, a):
    """
    >>> except_as_raise_with_empty_except(None, TypeError)
    1
    >>> except_as_raise_with_empty_except(TypeError('test'), TypeError)
    >>> except_as_raise_with_empty_except(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> except_as_raise_with_empty_except(None, TypeError)
    1
    """
    try:
        if x:
            raise x
        b = 1
    except a as b:  # previously raised UnboundLocalError
        pass
    try:
        print(b)  # raises UnboundLocalError if except clause was executed
    except UnboundLocalError:
        if not x:
            print("unexpected UnboundLocalError raised!")
    else:
        if x:
            print("expected UnboundLocalError not raised!")


def except_as_deletes_target_in_gen(x, a):
    """
    >>> list(except_as_deletes_target_in_gen(None, TypeError))
    [(1, 1), (2, 1), (5, 1)]
    >>> list(except_as_deletes_target_in_gen(TypeError('test'), TypeError))
    [(1, 1), 3, 6]
    >>> list(except_as_deletes_target_in_gen(ValueError('test'), TypeError))
    [(1, 1), (4, 1), (5, 1)]
    """
    b = 1
    try:
        i = 1
        yield (1, b)
        if x:
            raise x
        yield (2, b)
    except a as b:
        i = 2
        assert isinstance(b, a)
        yield 3
    except:
        yield (4, b)
    try:
        yield (5, b)
    except UnboundLocalError:
        yield 6


### Py3 feature tests

def print_function(*args):
    """
    >>> print_function(1,2,3)
    1 2 3
    """
    print(*args) # this isn't valid Py2 syntax


def exec3_function(cmd):
    """
    >>> exec3_function('a = 1+1')['a']
    2
    """
    g = {}
    l = {}
    exec(cmd, g, l)
    return l


def exec2_function(cmd):
    """
    >>> exec2_function('a = 1+1')['a']
    2
    """
    g = {}
    exec(cmd, g)
    return g


EXEC_GLOBAL = [5]

def exec1_function(cmd):
    """
    >>> exec1_function('EXEC_GLOBAL.append(1)')
    [1]
    """
    old = len(EXEC_GLOBAL)
    exec(cmd)
    return EXEC_GLOBAL[old:]


ustring = "abcdefg"

def unicode_literals():
    """
    >>> print( unicode_literals() )
    True
    abcdefg
    """
    print(isinstance(ustring, unicode) or type(ustring))
    return ustring


def non_ascii_unprefixed_str():
    u"""
    >>> s = non_ascii_unprefixed_str()
    >>> isinstance(s, bytes)
    False
    >>> len(s)
    3
    """
    s = 'ø\x20\u0020'
    assert isinstance(s, unicode)
    return s


def non_ascii_raw_str():
    u"""
    >>> s = non_ascii_raw_str()
    >>> isinstance(s, bytes)
    False
    >>> len(s)
    11
    """
    s = r'ø\x20\u0020'
    assert isinstance(s, unicode)
    return s


def non_ascii_raw_prefixed_unicode():
    u"""
    >>> s = non_ascii_raw_prefixed_unicode()
    >>> isinstance(s, bytes)
    False
    >>> len(s)
    11
    """
    s = ru'ø\x20\u0020'
    assert isinstance(s, unicode)
    return s


def str_type_is_unicode():
    """
    >>> str_type, s = str_type_is_unicode()
    >>> isinstance(s, type(ustring)) or (s, str_type)
    True
    >>> isinstance(s, str_type) or (s, str_type)
    True
    >>> isinstance(ustring, str_type) or str_type
    True
    """
    cdef str s = 'abc'
    return str, s


def loop_over_unicode_literal():
    """
    >>> print( loop_over_unicode_literal() )
    Py_UCS4
    """
    # Py_UCS4 can represent any Unicode character
    for uchar in 'abcdefg':
        assert uchar in 'abcdefg'
    return cython.typeof(uchar)


def list_comp():
    """
    >>> list_comp()
    [0, 4, 8]
    """
    x = 'abc'
    result = [x*2 for x in range(5) if x % 2 == 0]
    assert x == 'abc' # don't leak in Py3 code
    return result


def list_comp_iterable(it):
    """
    >>> list_comp_iterable([])
    []
    >>> list_comp_iterable([0])
    [0]
    >>> list_comp_iterable([1])
    []
    >>> list_comp_iterable([0, 1])
    [0]
    >>> list_comp_iterable([2])
    [4]
    >>> list_comp_iterable(range(5))
    [0, 4, 8]
    """
    x = 'abc'
    result = [x*2 for x in it if x % 2 == 0]
    assert x == 'abc' # don't leak in Py3 code
    return result


def list_comp_with_lambda():
    """
    >>> list_comp_with_lambda()
    [0, 4, 8]
    """
    x = 'abc'
    result = [x*2 for x in range(5) if (lambda x:x % 2)(x) == 0]
    assert x == 'abc' # don't leak in Py3 code
    return result


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


module_level_lc = [ module_level_loopvar*2 for module_level_loopvar in range(4) ]
def list_comp_module_level():
    """
    >>> module_level_lc
    [0, 2, 4, 6]
    >>> module_level_loopvar         # doctest: +ELLIPSIS
    Traceback (most recent call last):
    NameError: ...name 'module_level_loopvar' is not defined
    """


module_level_list_genexp = list(module_level_genexp_loopvar*2 for module_level_genexp_loopvar in range(4))
def genexpr_module_level():
    """
    >>> module_level_list_genexp
    [0, 2, 4, 6]
    >>> module_level_genexp_loopvar         # doctest: +ELLIPSIS
    Traceback (most recent call last):
    NameError: ...name 'module_level_genexp_loopvar' is not defined
    """


def list_comp_unknown_type(l):
    """
    >>> list_comp_unknown_type(range(5))
    [0, 4, 8]
    """
    return [x*2 for x in l if x % 2 == 0]


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


def set_comp():
    """
    >>> sorted(set_comp())
    [0, 4, 8]
    """
    x = 'abc'
    result = {x*2 for x in range(5) if x % 2 == 0}
    assert x == 'abc' # don't leak
    return result


def dict_comp():
    """
    >>> sorted(dict_comp().items())
    [(0, 0), (2, 4), (4, 8)]
    """
    x = 'abc'
    result = {x:x*2 for x in range(5) if x % 2 == 0}
    assert x == 'abc' # don't leak
    return result


# in Python 3, d.keys/values/items() are the iteration methods
@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
@cython.test_fail_if_path_exists(
    "//ForInStatNode")
def dict_iter(dict d):
    """
    >>> d = {'a' : 1, 'b' : 2, 'c' : 3}
    >>> keys, values, items = dict_iter(d)
    >>> sorted(keys)
    ['a', 'b', 'c']
    >>> sorted(values)
    [1, 2, 3]
    >>> sorted(items)
    [('a', 1), ('b', 2), ('c', 3)]

    >>> dict_iter({})
    ([], [], [])
    """
    keys = [ key for key in d.keys() ]
    values = [ value for value in d.values() ]
    items = [ item for item in d.items() ]
    return keys, values, items


@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
@cython.test_fail_if_path_exists(
    "//ForInStatNode")
def dict_iter_new_dict():
    """
    >>> dict_keys, keys, values, items = dict_iter_new_dict()
    >>> sorted(dict_keys)
    [11, 22, 33]
    >>> sorted(keys)
    [11, 22, 33]
    >>> sorted(values)
    [1, 2, 3]
    >>> sorted(items)
    [(11, 1), (22, 2), (33, 3)]
    """
    dict_keys = [ key for key in {11 : 1, 22 : 2, 33 : 3} ]
    keys = [ key for key in {11 : 1, 22 : 2, 33 : 3}.keys() ]
    values = [ value for value in {11 : 1, 22 : 2, 33 : 3}.values() ]
    items = [ item for item in {11 : 1, 22 : 2, 33 : 3}.items() ]
    return dict_keys, keys, values, items


def int_literals():
    """
    >>> int_literals()
    long
    long
    unsigned long
    unsigned long
    """
    print(cython.typeof(1L))
    print(cython.typeof(10000000000000L))
    print(cython.typeof(1UL))
    print(cython.typeof(10000000000000UL))


def annotation_syntax(a: "test new test", b : "other" = 2, *args: "ARGS", **kwargs: "KWARGS") -> "ret":
    """
    >>> annotation_syntax(1)
    3
    >>> annotation_syntax(1,3)
    4

    >>> len(annotation_syntax.__annotations__)
    5
    >>> print(annotation_syntax.__annotations__['a'])
    test new test
    >>> print(annotation_syntax.__annotations__['b'])
    other
    >>> print(annotation_syntax.__annotations__['args'])
    ARGS
    >>> print(annotation_syntax.__annotations__['kwargs'])
    KWARGS
    >>> print(annotation_syntax.__annotations__['return'])
    ret
    """
    result : int = a + b

    return result


async def async_def_annotations(x: 'int') -> 'float':
    """
    >>> ret, arg = sorted(async_def_annotations.__annotations__.items())
    >>> print(ret[0]); print(ret[1])
    return
    float
    >>> print(arg[0]); print(arg[1])
    x
    int
    """
    return float(x)
