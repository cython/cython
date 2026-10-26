############################################################################
# Frozen Dictionary Objects (Python 3.15+)
# Backported to older Python versions by falling back to 'dict'.
############################################################################

cdef extern from "Python.h":
    # PyTypeObject PyFrozenDict_Type
    # This instance of PyTypeObject represents the Python frozen dictionary type.
    # This is the same object as frozendict in the Python layer.

    bint PyAnyDict_Check "__Pyx_PyAnyDict_Check" (object p) noexcept
    # Return true if p is a dict object, a frozendict object, or an instance of a subtype
    # of the dict or frozendict type.
    # This function always succeeds.

    bint PyAnyDict_CheckExact "__Pyx_PyAnyDict_CheckExact" (object p) noexcept
    # Return true if p is a dict object or a frozendict object, but not an instance
    # of a subtype of the dict or frozendict type.
    # This function always succeeds.

    bint PyFrozenDict_Check "__Pyx_PyFrozenDict_Check" (object p) noexcept
    # Return true if p is a frozendict object or an instance of a subtype of the
    # frozendict type.
    # This function always succeeds.

    bint PyFrozenDict_CheckExact "__Pyx_PyFrozenDict_CheckExact" (object p) noexcept
    # Return true if p is a frozendict object, but not an instance of a subtype
    # of the frozendict type.
    # This function always succeeds.

    frozendict PyFrozenDict_New "__Pyx_PyFrozenDict_New" (object iterable)
    # Return a new frozendict from an iterable, or NULL on failure with an exception set.
    # Create an empty dictionary if iterable is NULL.

    frozendict PyFrozenDict_NewEmpty "__Pyx_PyFrozenDict_NewEmpty" ()
    # Return a new frozendict from an iterable, or NULL on failure with an exception set.
    # Create an empty dictionary if iterable is NULL.
