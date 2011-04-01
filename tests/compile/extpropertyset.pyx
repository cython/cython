# mode: compile

cdef class Spam:

    property eggs:

        def __set__(self, x):
            pass
