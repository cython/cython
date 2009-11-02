def spam(*args):
    """
    >>> spam()
    Args: ()
    >>> spam(42)
    Args: (42,)
    >>> spam("one", 2, "buckle my shoe")
    Args: ('one', 2, 'buckle my shoe')
    """
    print u"Args:", args
