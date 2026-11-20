# mode: error

cdef class A:

    @property
    def fortytwo(self):
        return self.fortytwo()

    def fortytwo(self):
        return 42

_ERRORS = u"""
5:4: Property hides existing attribute 'fortytwo'
"""

