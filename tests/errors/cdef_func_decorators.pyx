# mode: error
# tag: decorator

from functools import wraps

@wraps
cdef cant_be_decoratored():
    pass

@wraps
cpdef also_cant_be_decorated():
    pass

cdef class C:
    @wraps
    cdef still_cant_be_decorated(self):
        pass

    @property
    cdef property_only_works_for_extern_classes(self):
        pass

    @wraps
    cpdef also_still_cant_be_decorated(self):
        pass

    @wraps
    @wraps
    cdef two_is_just_as_bad_as_one(self):
        pass

_ERRORS = """
6:0: Cdef functions cannot take arbitrary decorators.
10:0: Cdef functions cannot take arbitrary decorators.
15:4: Cdef functions cannot take arbitrary decorators.
19:4: Cdef functions cannot take arbitrary decorators.
23:4: Cdef functions cannot take arbitrary decorators.
27:4: Cdef functions cannot take arbitrary decorators.
"""
