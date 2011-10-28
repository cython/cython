# ticket: 470

__doc__ = u"""
>>> func(**{'a' : 7})
True
>>> func(**SubDict())
True

>>> call_non_dict_test()
True
>>> call_non_dict_test_kw()
True

>>> call_sub_dict_test()
True
>>> call_sub_dict_test_kw()
True
"""

import sys

if sys.version_info >= (2,6):
    __doc__ += u"""
>>> func(**NonDict())
True
"""

def func(**kwargs):
    return type(kwargs) is dict and kwargs['a'] == 7


class NonDict(object):
   def __getitem__(self, k):
       assert k == 'a'
       return 7
   def keys(self):
       return ['a']

def call_non_dict_test():
    return func(**NonDict())

def call_non_dict_test_kw():
    return func(b=5, **NonDict())


class SubDict(dict):
    def __init__(self):
        self['a'] = 7

def call_sub_dict_test():
    return func(**SubDict())

def call_sub_dict_test_kw():
    return func(b=5, **SubDict())
