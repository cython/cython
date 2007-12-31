cdef class Spam:

    property eggs:
    
        def __get__(self):
            pass

cdef void tomato():
    cdef Spam spam
    cdef object lettuce
    lettuce = spam.eggs

