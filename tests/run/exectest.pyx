__doc__ = """# no unicode string, not tested in Python3!
#>>> a
#Traceback (most recent call last):
#NameError: name 'a' is not defined
#>>> test_module_scope()
#>>> a

>>> test_dict_scope1()
2

>>> d = {}
>>> test_dict_scope2(d)
>>> print d['b']
2

>>> d1 = {}
>>> test_dict_scope3(d1, d1)
>>> print d1['b']
2

>>> d1, d2 = {}, {}
>>> test_dict_scope3(d1, d2)
>>> print d1.get('b'), d2.get('b')
None 2

>>> d1, d2 = {}, {}
>>> test_dict_scope3(d1, d2)
>>> print d1.get('b'), d2.get('b')
None 2

>>> d1, d2 = dict(a=11), dict(c=5)
>>> test_dict_scope_ref(d1, d2)
>>> print d1.get('b'), d2.get('b')
None 16

>>> d = dict(a=11, c=5)
>>> test_dict_scope_ref(d, d)
>>> print d['b']
16

>>> d = dict(seq = [1,2,3,4])
>>> add_iter = test_def(d, 'seq')
>>> list(add_iter())
[2, 3, 4, 5]

>>> # errors

>>> d1, d2 = {}, {}
>>> test_dict_scope_ref(d1, d2)
Traceback (most recent call last):
NameError: name 'a' is not defined
"""

#def test_module_scope():
#    exec "a=1+1"
#    return __dict__['a']

def test_dict_scope1():
    cdef dict d = {}
    exec "b=1+1" in d
    return d['b']

def test_dict_scope2(d):
    exec "b=1+1" in d

def test_dict_scope3(d1, d2):
    exec "b=1+1" in d1, d2

def test_dict_scope_ref(d1, d2):
    exec "b=a+c" in d1, d2

def test_def(d, varref):
    exec """
def test():
    for x in %s:
        yield x+1
""" % varref in d
    return d['test']
