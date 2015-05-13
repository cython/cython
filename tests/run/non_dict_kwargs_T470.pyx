# mode: run
# ticket: 470


def func(**kwargs):
    """
    >>> func(**{'a' : 7})
    True
    >>> func(**SubDict())
    True
    >>> func(**NonDict())
    True
    """
    return type(kwargs) is dict and kwargs['a'] == 7


class NonDict(object):
   def __getitem__(self, k):
       assert k == 'a'
       return 7
   def keys(self):
       return ['a']

def call_non_dict_test():
    """
    >>> call_non_dict_test()
    True
    """
    return func(**NonDict())

def call_non_dict_test_kw():
    """
    >>> call_non_dict_test_kw()
    True
    """
    return func(b=5, **NonDict())


class SubDict(dict):
    def __init__(self):
        self['a'] = 7

def call_sub_dict_test():
    """
    >>> call_sub_dict_test()
    True
    """
    return func(**SubDict())

def call_sub_dict_test_kw():
    """
    >>> call_sub_dict_test_kw()
    True
    """
    return func(b=5, **SubDict())
