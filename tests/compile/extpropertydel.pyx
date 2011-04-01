# mode: compile

cdef class Spam:

    property eggs:

        def __del__(self):
            pass
