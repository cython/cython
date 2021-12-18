# mode: error
# ticket: t264
# tag: property, decorator


from functools import wraps


def wrap_func(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print("WRAPPED")
        return f(*args, **kwargs)
    return wrap


cdef class Prop:
    @property
    @wrap_func
    def prop1(self):
        return 1

    @property
    def prop2(self):
        return 2

    @wrap_func
    @prop2.setter
    def prop2(self, value):
        pass

    @prop2.setter
    @wrap_func
    def prop2(self, value):
        pass

    @prop2.setter
    def other_name(self, value):
        pass


_ERRORS = """
19:4: Property methods with additional decorators are not supported
27:4: Property methods with additional decorators are not supported
33:4: Property methods with additional decorators are not supported
37:4: Mismatching property names, expected 'prop2', got 'other_name'
"""
