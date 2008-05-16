__doc__ = u"""
    >>> empty()
    {}
    >>> keyvalue(1, 2)
    {1: 2}

    >>> keyvalues(1, 2, 3, 4)
    {1: 2, 3: 4}
    >>> keyvalues2(1, 2, 3, 4)
    {1: 2, 3: 4}

    >>> len(constant())
    2
    >>> print(constant()['parrot'])
    resting
    >>> print(constant()['answer'])
    42
"""

def empty():
    d = {}
    return d

def keyvalue(key, value):
    d = {key:value}
    return d

def keyvalues(key1, value1, key2, value2):
    d = {key1:value1, key2:value2}
    return d

def keyvalues2(key1, value1, key2, value2):
    d = {key1:value1, key2:value2,}
    return d

def constant():
    d = {u"parrot":u"resting", u"answer":42}
    return d
