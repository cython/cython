cdef class Spam:

    property eggs:
    
        def __get__(self):
            return 42

def tomato():
    """
    >>> tomato()
    42
    """
    cdef Spam spam
    cdef object lettuce
    spam = Spam()
    lettuce = spam.eggs
    return lettuce
