__doc__ = u"""
    >>> spam()
    Args: ()
    >>> spam(42)
    Args: (42,)
    >>> spam("one", 2, "buckle my shoe")
    Args: ('one', 2, 'buckle my shoe')
"""

def spam(*args):
    print u"Args:", args

