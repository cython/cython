cdef class Spam:

    property eggs:
    
        def __get__(self):
            """
            This is the docstring for Spam.eggs.__get__
            """
            return 42

def tomato():
    """
    >>> tomato()
    42

    >>> lines = __test__.keys()
    >>> len(lines)
    2
    >>> 'Spam.eggs.__get__ (line 5)' in lines
    True
    >>> 'tomato (line 11)' in lines
    True
    """
    cdef Spam spam
    cdef object lettuce
    spam = Spam()
    lettuce = spam.eggs
    return lettuce
