__doc__ = u"""
>>> tomato()
42
"""

cdef class Spam:

    property eggs:
    
        def __get__(self):
            return 42

def tomato():
    cdef Spam spam
    cdef object lettuce
    spam = Spam()
    lettuce = spam.eggs
    return lettuce
