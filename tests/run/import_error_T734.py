# mode: run
# ticket: 734

def test_import_error():
    """
    >>> test_import_error()
    Traceback (most recent call last):
    ImportError: cannot import name xxx
    """
    from sys import xxx
