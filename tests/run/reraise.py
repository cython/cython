
def reraise():
    raise

def test_reraise():
    """
    >>> test_reraise()
    Traceback (most recent call last):
    ValueError: TEST
    """
    try:
        raise ValueError("TEST")
    except ValueError:
        raise

def test_reraise_indirect():
    """
    >>> test_reraise_indirect()
    Traceback (most recent call last):
    ValueError: TEST INDIRECT
    """
    try:
        raise ValueError("TEST INDIRECT")
    except ValueError:
        reraise()

def test_reraise_error():
    """
    >>> try: test_reraise_error()
    ... except (RuntimeError, TypeError): pass  # Py2, Py3, ...
    ... else: print("FAILED")
    """
    import sys
    if hasattr(sys, 'exc_clear'):  # Py2
        sys.exc_clear()
    raise
