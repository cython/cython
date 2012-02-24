def empty():
    """
    >>> empty()
    {}
    """
    d = {}
    return d

def keyvalue(key, value):
    """
    >>> keyvalue(1, 2)
    {1: 2}
    """
    d = {key:value}
    return d

def keyvalues(key1, value1, key2, value2):
    """
    >>> sorted(keyvalues(1, 2, 3, 4).items())
    [(1, 2), (3, 4)]
    """
    d = {key1:value1, key2:value2}
    return d

def keyvalues2(key1, value1, key2, value2):
    """
    >>> sorted(keyvalues2(1, 2, 3, 4).items())
    [(1, 2), (3, 4)]
    """
    d = {key1:value1, key2:value2,}
    return d

def constant():
    """
    >>> len(constant())
    2
    >>> print(constant()['parrot'])
    resting
    >>> print(constant()['answer'])
    42
    """
    d = {u"parrot":u"resting", u"answer":42}
    return d

def dict_call():
    """
    >>> print(dict_call()['parrot'])
    resting
    >>> print(dict_call()['answer'])
    42
    """
    d = dict(parrot=u"resting", answer=42)
    return d

def dict_call_dict():
    """
    >>> print(dict_call_dict()['parrot'])
    resting
    >>> print(dict_call_dict()['answer'])
    42
    """
    d = dict(dict(parrot=u"resting", answer=42))
    return d

def dict_call_kwargs():
    """
    >>> print(dict_call_kwargs()['parrot1'])
    resting
    >>> print(dict_call_kwargs()['parrot2'])
    resting
    >>> print(dict_call_kwargs()['answer1'])
    42
    >>> print(dict_call_kwargs()['answer2'])
    42
    """
    kwargs = dict(parrot1=u"resting", answer1=42)
    d = dict(parrot2=u"resting", answer2=42, **kwargs)
    return d
