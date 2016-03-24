# mode: run
# tag: closure

def reassign_args(x, *args):
    """
    >>> reassign_args(1, [1,2,3,4])
    """
    a,args = args[0], args[1:]
    b = False
    if b:
        c = x.map_coefficients(lambda c: c(*args))
