# mode: run
# ticket: t3938
# tag: pep448

def t3938(x, l, m):
    """
    >>> l = [1,2,3]
    >>> m = [4,5,6]
    >>> x = 1
    >>> unpack_in_operator_starred_expressions(x, l, m)
    True
    >>> x = 10
    >>> unpack_in_operator_starred_expressions(x, l, m)
    False
    >>> unpack_in_operator_starred_expressions(x, l, [])
    False
    >>> unpack_in_operator_starred_expressions(x, [], [])
    False
    """
    return x in [*l, *m]
