__doc__ = u"""
>>> type(test_set_literal()) is _set
True
>>> sorted(test_set_literal())
[u'a', u'b', 1]

>>> type(test_set_add()) is _set
True
>>> sorted(test_set_add())
[u'a', 1]

>>> type(test_set_list_comp()) is _set
True
>>> sorted(test_set_list_comp())
[0, 1, 2]

>>> type(test_set_clear()) is _set
True
>>> list(test_set_clear())
[]

>>> type(test_set_pop()) is _set
True
>>> list(test_set_pop())
[]

>>> type(test_set_discard()) is _set
True
>>> sorted(test_set_discard())
[u'12', 233]
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"u'", u"'").replace(u'u"', u'"')

# Py2.3 doesn't have the 'set' builtin type, but Cython does :)
_set = set

def test_set_literal():
    cdef set s1 = {1,u'a',1,u'b',u'a'}
    return s1

def test_set_add():
    cdef set s1
    s1 = set([1])
    s1.add(1)
    s1.add(u'a')
    s1.add(1)
    return s1

def test_set_clear():
    cdef set s1
    s1 = set([1])
    s1.clear()
    return s1

def test_set_list_comp():
    cdef set s1
    s1 = set([i%3 for i in range(5)])
    return s1

def test_set_pop():
    cdef set s1
    s1 = set()
    s1.add(u'2')
    two = s1.pop()
    return s1

def test_set_discard():
    cdef set s1
    s1 = set()
    s1.add(u'12')
    s1.add(3)
    s1.add(233)
    s1.discard(u'3')
    s1.discard(3)
    return s1

def sorted(it):
    # Py3 can't compare strings to ints
    chars = []
    nums = []
    for item in it:
        if type(item) is int:
            nums.append(item)
        else:
            chars.append(item)
    nums.sort()
    chars.sort()
    return chars+nums
