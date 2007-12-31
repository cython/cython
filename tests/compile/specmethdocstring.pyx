cdef class C:
    def __init__(self):
        "This is an unusable docstring."
    property foo:
        def __get__(self):
            "So is this."
        def __set__(self, x):
            "And here is another one."
