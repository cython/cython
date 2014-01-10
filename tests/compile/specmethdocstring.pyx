# mode: compile

cdef class C:
    def __cinit__(self):
        "This is an unusable docstring."
    def __init__(self):
        "This is an unusable docstring."
    def __dealloc__(self):
        "This is an unusable docstring."
    def __richcmp__(self, other, int op):
        "This is an unusable docstring."
    def __nonzero__(self):
        "This is an unusable docstring."
        return False
    def __contains__(self, other):
        "This is an unusable docstring."

    property foo:
        def __get__(self):
            "So is this."
        def __set__(self, x):
            "And here is another one."

    def __div__(self, other):
        "usable docstring"
    def __iter__(self):
        "usable docstring"
        return False
    def __next__(self):
        "usable docstring"
        return False

