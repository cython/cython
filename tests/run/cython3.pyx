# cython: language_level=3
# mode: run
# tag: generators, python3

cimport cython

__doc__ = """
>>> items = sorted(locals_function(1).items())
>>> for item in items:
...     print('%s = %r' % item)
a = 1
b = 2
x = u'abc'
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(" u'", " '")

def locals_function(a, b=2):
    x = 'abc'
    return locals()


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
        pass
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

def list_comp_with_lambda():
    """
    >>> list_comp_with_lambda()
    [0, 4, 8]
    """
    x = 'abc'
    result = [x*2 for x in range(5) if (lambda x:x % 2)(x) == 0]
    assert x == 'abc' # don't leak in Py3 code
    return result

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

def annotation_syntax(a : "test", b : "other" = 2) -> "ret":
    """
    >>> annotation_syntax(1)
    3
    >>> annotation_syntax(1,3)
    4
    """
    return a+b
