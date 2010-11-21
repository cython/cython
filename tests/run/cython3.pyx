# cython: language_level=3

cimport cython

try:
    sorted
except NameError:
    def sorted(seq):
        seq = list(seq)
        seq.sort()
        return seq

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

ustring = "abcdefg"

def unicode_literals():
    """
    >>> print( unicode_literals() )
    True
    abcdefg
    """
    print(isinstance(ustring, unicode) or type(ustring))
    return ustring

def list_comp():
    """
    >>> list_comp()
    [0, 4, 8]
    """
    x = 'abc'
    result = [x*2 for x in range(5) if x % 2 == 0]
    assert x == 'abc' # don't leak in Py3 code
    return result

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
    "//WhileStatNode/SimpleCallNode",
    "//WhileStatNode/SimpleCallNode/NameNode")
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
    """
    keys = [ key for key in d.keys() ]
    values = [ value for value in d.values() ]
    items = [ item for item in d.items() ]
    return keys, values, items

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
