# cython: linetrace=true

fn void foo(i32 err) except * nogil:
    with gil:
        raise ValueError(err)


# Test from gh-4637
def handler(i32 err):
    """
    >>> handler(0)
    All good
    >>> handler(1)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: 1
    """
    if (err % 2):
        with nogil:
            foo(err)
    else:
        print("All good")
