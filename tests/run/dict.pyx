# mode: run

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


def items_of_dict_call():
    """
    >>> items_of_dict_call()
    [('answer1', 42), ('answer2', 42), ('parrot1', 'resting'), ('parrot2', 'resting')]
    """
    kwargs = dict(parrot1="resting", answer1=42)
    items = dict(kwargs.items(), parrot2="resting", answer2=42, **kwargs).items()
    return sorted(items)


def item_creation_sideeffect(L, sideeffect, unhashable):
    """
    >>> def sideeffect(x):
    ...     L.append(x)
    ...     return x
    >>> def unhashable(x):
    ...     L.append(x)
    ...     return [x]

    >>> L = []
    >>> item_creation_sideeffect(L, sideeffect, unhashable)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...unhashable...
    >>> L
    [2, 4]

    >>> L = []
    >>> {1:2, sideeffect(2): 3, 3: 4, unhashable(4): 5, sideeffect(5): 6}  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...unhashable...
    >>> L
    [2, 4, 5]
    """
    return {1:2, sideeffect(2): 3, 3: 4, unhashable(4): 5, sideeffect(5): 6}


def dict_unpacking_not_for_arg_create_a_copy():
    """
    >>> dict_unpacking_not_for_arg_create_a_copy()
    [('a', 'modified'), ('b', 'original')]
    [('a', 'original'), ('b', 'original')]
    """
    data = {'a': 'original', 'b': 'original'}

    func = lambda: {**data}

    call_once = func()
    call_once['a'] = 'modified'

    call_twice = func()

    print(sorted(call_once.items()))
    print(sorted(call_twice.items()))

def from_keys_bound(dict d, val):
    """
    https://github.com/cython/cython/issues/5051
    Optimization of bound method calls was breaking classmethods
    >>> sorted(from_keys_bound({}, 100).items())
    [('a', 100), ('b', 100)]
    >>> sorted(from_keys_bound({}, None).items())
    [('a', None), ('b', None)]
    """
    if val is not None:
        return d.fromkeys(("a", "b"), val)
    else:
        return d.fromkeys(("a", "b"))
