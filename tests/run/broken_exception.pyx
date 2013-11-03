
import sys

def exception_creates_invalid_instance():
    """
    >>> print( exception_creates_invalid_instance() )
    OK
    """
    class MyException(Exception):
        def __new__(cls, *args):
            return object()

    if sys.version_info[0] >= 3:
        expected_error = TypeError
    else:
        expected_error = MyException

    try:
        raise MyException
    except expected_error:
        return "OK"
