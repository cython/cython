
module_name = __name__

def in_module():
    """
    >>> print(in_module())
    mod__name__
    """
    return module_name

def in_function():
    """
    >>> print(in_function())
    mod__name__
    """
    return __name__
