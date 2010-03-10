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
    >>> sorted(__test__.keys())
    [u'Spam.eggs.__get__ (line 5)', u'tomato (line 11)']
    """
    cdef Spam spam
    cdef object lettuce
    spam = Spam()
    lettuce = spam.eggs
    return lettuce
