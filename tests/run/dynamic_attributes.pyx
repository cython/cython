# mode: run

cimport cython

cdef class Spam:
    cdef dict __dict__

cdef class SuperSpam(Spam):
    pass

cdef class MegaSpam:
    pass

cdef public class UltraSpam [type UltraSpam_Type, object UltraSpam_Object]:
    cdef dict __dict__


cdef class OwnProperty1:
    """
    >>> obj = OwnProperty1()
    >>> assert obj.__dict__ == {'a': 123}
    """
    @property
    def __dict__(self):
        return {'a': 123}


cdef class OwnProperty2:
    """
    >>> obj = OwnProperty2()
    >>> assert obj.__dict__ == {'a': 123}
    """
    property __dict__:
        def __get__(self):
            return {'a': 123}


def test_class_attributes():
    """
    >>> test_class_attributes()
    'bar'
    """
    o = Spam()
    o.foo = "bar"
    return o.foo

def test_subclass_attributes():
    """
    >>> test_subclass_attributes()
    'bar'
    """
    o = SuperSpam()
    o.foo = "bar"
    return o.foo

def test_defined_class_attributes():
    """
    >>> test_defined_class_attributes()
    'bar'
    """
    o = MegaSpam()
    o.foo = "bar"
    return o.foo

def test_public_class_attributes():
    """
    >>> test_public_class_attributes()
    'bar'
    """
    o = UltraSpam()
    o.foo = "bar"
    return o.foo
