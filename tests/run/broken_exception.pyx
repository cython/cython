
def exception_creates_invalid_instance():
    """
    >>> print( exception_creates_invalid_instance() )
    OK
    """
    class MyException(Exception):
        def __new__(cls, *args):
            return object()

    try:
        raise MyException
    except TypeError:
        return "OK"
