# cython: safe_property_autocomplete=True

cimport cython
import sys

# For testing purposes we need to make it so Cython believes the interpreter
# is interactive.
cdef extern from *:
    """
    #if __PYX_LIMITED_VERSION_HEX >= 0x030F0000 && PY_VERSION_HEX > 0x030F00B2
    static int __pyx_interpreter_is_interactive;
    #endif
    """
    int __pyx_interpreter_is_interactive

cdef int trick_cython_into_believing_interpreter_is_interactive():
   global __pyx_interpreter_is_interactive
   value, __pyx_interpreter_is_interactive = __pyx_interpreter_is_interactive, 1
   return value;

# Test access through cython call
def get_guarded_fail_cy(inst):
    return inst.p_guarded_fail

def get_unguarded_fail_cy(inst):
    return inst.q_unguarded_fail

# Test access through Python call
exec("""
def get_guarded_fail_py(inst):
    return inst.p_guarded_fail

def get_unguarded_fail_py(inst):
    return inst.q_unguarded_fail
""", globals())

assert not trick_cython_into_believing_interpreter_is_interactive()

cdef class FailableProperties:
    """
    >>> import rlcompleter

    >>> inst = FailableProperties()
    >>> inst.set_fail(KeyError)
    >>> inst.p_guarded_fail
    Traceback (most recent call last):
       ...
    KeyError: 'Something bad happened'
    >>> get_guarded_fail_cy(inst)
    Traceback (most recent call last):
       ...
    KeyError: 'Something bad happened'
    >>> get_guarded_fail_py(inst)
    Traceback (most recent call last):
       ...
    KeyError: 'Something bad happened'
    >>> get_unguarded_fail_cy(inst)
    Traceback (most recent call last):
       ...
    KeyError: 'Something bad happened'
    >>> get_unguarded_fail_py(inst)
    Traceback (most recent call last):
       ...
    KeyError: 'Something bad happened'
    >>> completer = rlcompleter.Completer(dict(inst=inst))
    >>> completer.attr_matches("inst.p_")
    ['inst.p_aardvark', 'inst.p_guarded_fail', 'inst.p_zebra']

    # Note that on AttributeErrors Python sometimes adds "did you mean". This is fine.
    >>> inst.set_fail(AttributeError)
    >>> inst.p_guarded_fail  # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    AttributeError: Something bad happened...
    >>> get_guarded_fail_cy(inst)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    AttributeError: Something bad happened...
    >>> get_guarded_fail_py(inst)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    AttributeError: Something bad happened...
    >>> get_unguarded_fail_cy(inst)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    AttributeError: Something bad happened...
    >>> get_unguarded_fail_py(inst)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    AttributeError: Something bad happened...
    >>> completer = rlcompleter.Completer(dict(inst=inst))
    >>> completer.attr_matches("inst.p_")
    ['inst.p_aardvark', 'inst.p_guarded_fail', 'inst.p_zebra']
    """
    cdef fail_with_type

    def set_fail(self, tp):
        self.fail_with_type = tp

    @property
    def p_aardvark(self):
        return 1
    
    @property
    def p_guarded_fail(self):
        if self.fail_with_type is not None:
            raise self.fail_with_type("Something bad happened")

    @property
    def p_zebra(self):
        return 1
    
    @property
    def q_aardvark(self):
        return 1

    @cython.safe_property_autocomplete(False)
    @property
    def q_unguarded_fail(self):
        if self.fail_with_type is not None:
            raise self.fail_with_type("Something bad happened")

    @property
    def q_zebra(self):
        return 1

class MyBaseException(BaseException):
    pass

__doc__ = ""

if (sys.version_info < (3, 13, 14) or
        (sys.version_info[:2] == (3, 14) and sys.version_info < (3, 14, 7))):
    # On these versions we can check the behaviour of unguarded fails
    # and BaseExceptions because we implement the guard rather than it
    # being in rlcompleter.
    __doc__ += """
    >>> import rlcompleter

    >>> inst = FailableProperties()
    >>> completer = rlcompleter.Completer(dict(inst=inst))

    >>> inst.set_fail(KeyError)

    # No catching from unguarded property
    >>> completer.attr_matches("inst.q_")
    Traceback (most recent call last):
       ...
    KeyError: 'Something bad happened'

    >>> inst.set_fail(MyBaseException)  # BaseException
    >>> inst.p_guarded_fail
    Traceback (most recent call last):
       ...
    autocomplete_properties.MyBaseException: Something bad happened
    >>> get_guarded_fail_cy(inst)
    Traceback (most recent call last):
       ...
    autocomplete_properties.MyBaseException: Something bad happened
    >>> get_guarded_fail_py(inst)
    Traceback (most recent call last):
       ...
    autocomplete_properties.MyBaseException: Something bad happened
    >>> get_unguarded_fail_cy(inst)
    Traceback (most recent call last):
       ...
    autocomplete_properties.MyBaseException: Something bad happened
    >>> get_unguarded_fail_py(inst)
    Traceback (most recent call last):
       ...
    autocomplete_properties.MyBaseException: Something bad happened

    # Our guards don't handle base exceptions
    >>> completer.attr_matches("inst.p_")
    Traceback (most recent call last):
       ...
    autocomplete_properties.MyBaseException: Something bad happened
    >>> completer.attr_matches("inst.q_")
    Traceback (most recent call last):
       ...
    autocomplete_properties.MyBaseException: Something bad happened
    """
