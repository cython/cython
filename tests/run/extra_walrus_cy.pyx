# mode: run

def return_x(x):
    return x

def for_from_in_try(x):
    """
    >>> for_from_in_try(10)
    'Except return 10'
    >>> for_from_in_try(0)
    'Normal return 0'
    """
    try:
        for 0 <= _ < (a := return_x(x)):
            raise RuntimeError
        
        return f'Normal return {a}'
    except Exception:
        return f'Except return {a}'
