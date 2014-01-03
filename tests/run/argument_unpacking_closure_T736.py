# mode: run
# ticket: 736
# tag: default arguments, closure

def default_args_for_closure(a=1, b=2):
    """
    >>> default_args_for_closure()()
    (1, 2)
    >>> default_args_for_closure(1, 2)()
    (1, 2)
    >>> default_args_for_closure(2)()
    (2, 2)
    >>> default_args_for_closure(8,9)()
    (8, 9)
    >>> default_args_for_closure(7, b=6)()
    (7, 6)
    >>> default_args_for_closure(a=5, b=4)()
    (5, 4)
    >>> default_args_for_closure(b=5, a=6)()
    (6, 5)
    """
    def func():
        return a,b
    return func
