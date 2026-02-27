class MySpecialException(Exception):
    def method(self):
        return "method"
    
    def __neg__(self):
        return "neg"

    def __abs__(self):
        return "abs"

    def __len__(self):
        return 100

    def __add__(self, other):
        return f"add {other}"

    # This overrides a method of BaseException
    def with_traceback(self, tb):
        return "ecart"

def test_exception_method():
    """
    >>> test_exception_method()
    'method'
    """
    try:
        raise MySpecialException()
    except MySpecialException as e:
        return e.method()

def test_exception_minus():
    """
    >>> test_exception_minus()
    'neg'
    """
    try:
        raise MySpecialException()
    except MySpecialException as e:
        return -e

def test_exception_abs():
    """
    >>> test_exception_abs()
    'abs'
    """
    try:
        raise MySpecialException()
    except MySpecialException as e:
        return abs(e)

def test_exception_len():
    """
    >>> test_exception_len()
    100
    """
    try:
        raise MySpecialException()
    except MySpecialException as e:
        return len(e)


def test_exception_sum():
    """
    >>> test_exception_sum()
    'add 1'
    """
    try:
        raise MySpecialException()
    except MySpecialException as e:
        return e+1

def test_known_method():
    """
    >>> test_known_method()
    'ecart'
    """
    try:
        raise MySpecialException()
    except MySpecialException as e:
        return e.with_traceback(None)
