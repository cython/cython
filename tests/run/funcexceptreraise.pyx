import sys

def reraise(f, exc):
    """
    >>> def f(exc): raise exc
    >>> reraise(f, TypeError)
    Traceback (most recent call last):
    TypeError

    >>> def f(exc): raise exc('hiho')
    >>> reraise(f, TypeError)
    Traceback (most recent call last):
    TypeError: hiho
    """
    try:
        f(exc)
    except:
        assert sys.exc_info()[0] is exc, str(sys.exc_info()[1])
        raise

def reraise_original(f, exc, raise_catch):
    """
    >>> def f(exc): raise exc
    >>> def raise_catch_py():
    ...     try: raise ValueError
    ...     except: pass

    >>> reraise_original(f, TypeError, raise_catch_py)
    Traceback (most recent call last):
    TypeError

    >>> reraise_original(f, TypeError, raise_catch_cy)
    Traceback (most recent call last):
    TypeError

    >>> reraise_original(f, TypeError, raise_catch_cy_non_empty)
    Traceback (most recent call last):
    TypeError
    """
    try:
        f(exc)
    except:
        raise_catch()
        assert sys.exc_info()[0] is exc, str(sys.exc_info()[1])
        raise


def raise_catch_cy():
    try: raise ValueError
    except: pass

def raise_catch_cy_non_empty():
    try: raise ValueError
    except:
        a = 1+1
