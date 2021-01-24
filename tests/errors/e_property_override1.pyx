# mode: error

cdef class A:

    def fortytwo(self):
        return 42

    @property
    def fortytwo(self):
        return self.fortytwo()

_ERRORS = u"""
8:4: Duplicate property decorator and other class attribute name 'fortytwo'
"""

