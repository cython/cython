# mode: run
# tag: generators unreachable

def with_yield_removed():
    """
    >>> o = with_yield_removed()
    >>> list(o)
    []
    """
    return
    yield
