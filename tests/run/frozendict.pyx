# mode: run

def empty():
    """
    >>> not empty()
    True
    """
    d = frozendict()
    return d


def frozendict_call():
    """
    >>> print(frozendict_call()['parrot'])
    resting
    >>> print(frozendict_call()['answer'])
    42
    """
    d = frozendict(parrot=u"resting", answer=42)
    return d


def frozendict_call_dict():
    """
    >>> print(frozendict_call_dict()['parrot'])
    resting
    >>> print(frozendict_call_dict()['answer'])
    42
    """
    d = frozendict(dict(parrot=u"resting", answer=42))
    return d


def frozendict_call_frozendict():
    """
    >>> print(frozendict_call_frozendict()['parrot'])
    resting
    >>> print(frozendict_call_frozendict()['answer'])
    42
    """
    d = frozendict(frozendict(parrot=u"resting", answer=42))
    return d


def frozendict_call_kwargs():
    """
    >>> print(frozendict_call_kwargs()['parrot1'])
    resting
    >>> print(frozendict_call_kwargs()['parrot2'])
    resting
    >>> print(frozendict_call_kwargs()['answer1'])
    42
    >>> print(frozendict_call_kwargs()['answer2'])
    42
    """
    kwargs = frozendict(parrot1=u"resting", answer1=42)
    d = frozendict(parrot2=u"resting", answer2=42, **kwargs)
    return d


def items_of_frozendict_call():
    """
    >>> items_of_frozendict_call()
    [('answer1', 42), ('answer2', 42), ('parrot1', 'resting'), ('parrot2', 'resting')]
    """
    kwargs = frozendict(parrot1="resting", answer1=42)
    items = frozendict(kwargs.items(), parrot2="resting", answer2=42, **kwargs).items()
    return sorted(items)
