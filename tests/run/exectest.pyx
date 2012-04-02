# -*- coding: utf-8 -*-

__doc__ = u"""
#>>> a
#Traceback (most recent call last):
#NameError: name 'a' is not defined
#>>> test_module_scope()
#>>> a

>>> test_dict_scope1()
2

>>> d = {}
>>> test_dict_scope2(d)
>>> d['b']
2

>>> d1 = {}
>>> test_dict_scope3(d1, d1)
>>> d1['b']
2

>>> d1, d2 = {}, {}
>>> test_dict_scope3(d1, d2)
>>> (d1.get('b'), d2.get('b'))
(None, 2)

>>> d1, d2 = {}, {}
>>> test_dict_scope3(d1, d2)
>>> (d1.get('b'), d2.get('b'))
(None, 2)

>>> d1, d2 = dict(a=11), dict(c=5)
>>> test_dict_scope_ref(d1, d2)
>>> (d1.get('b'), d2.get('b'))
(None, 16)

>>> d = dict(a=11, c=5)
>>> test_dict_scope_ref(d, d)
>>> d['b']
16

>>> d = dict(seq = [1,2,3,4])
>>> add_iter = test_def(d, 'seq')
>>> list(add_iter())
[2, 3, 4, 5]

>>> d = {}
>>> test_encoding(d, None)
>>> print(d['b'])
üöä

>>> d = {}
>>> test_encoding_unicode(d, None)
>>> print(d['b'])
üöä

>>> d = dict(a=1, c=3)
>>> test_compile(d)
>>> d['b']
4

>>> # errors

>>> d1, d2 = {}, {}
>>> test_dict_scope_ref(d1, d2)         # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'a' is not defined
"""

#def test_module_scope():
#    exec "a=1+1"
#    return __dict__['a']

def test_dict_scope1():
    cdef dict d = {}
    exec u"b=1+1" in d
    return d[u'b']

def test_dict_scope2(d):
    exec u"b=1+1" in d

def test_dict_scope3(d1, d2):
    exec u"b=1+1" in d1, d2

def test_dict_scope_ref(d1, d2):
    exec u"b=a+c" in d1, d2

def test_def(d, varref):
    exec u"""
def test():
    for x in %s:
        yield x+1
""" % varref in d
    return d[u'test']

import sys

def test_encoding(d1, d2):
    if sys.version_info[0] >= 3:
        s = "b = 'üöä'"
    else:
        s = "# -*- coding: utf-8 -*-" + "\n" + "b = u'üöä'"
    exec s in d1, d2

def test_encoding_unicode(d1, d2):
    if sys.version_info[0] >= 3:
        s = u"b = 'üöä'"
    else:
        s = u"b = u'üöä'"
    exec s in d1, d2

def test_compile(d):
    c = compile(u"b = a+c", u"<string>", u"exec")
    exec c in d
