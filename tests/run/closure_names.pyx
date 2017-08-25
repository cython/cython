# mode: run
# tag: closures
# ticket: gh-1797


def func():
    """
    >>> funcs = func()
    >>> [f(1) for f in funcs]
    ['eq', 'str', 'weakref', 'new', 'dict']
    """
    def __eq__(a):
        return 'eq'

    def __str__(a):
        return 'str'

    def __weakref__(a):
        return 'weakref'

    def __new__(a):
        return 'new'

    def __dict__(a):
        return 'dict'

    def list_from_gen(g):
        return list(g)

    # move into closure by using inside of generator expression
    return list_from_gen([__eq__, __str__, __weakref__, __new__, __dict__][i] for i in range(5))
