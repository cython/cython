# mode: compile

cdef class Spam:

    property eggs:

        "Ova"

        def __get__(self):
            pass

        def __set__(self, x):
            pass

        def __del__(self):
            pass

