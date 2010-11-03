# cython: language_level=3

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
