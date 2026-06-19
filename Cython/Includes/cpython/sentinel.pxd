############################################################################
# Sentinel Objects (Python 3.15+)
############################################################################

cdef extern from "Python.h":
    # PyTypeObject PySentinel_Type
    # This instance of PyTypeObject represents the Python 'sentinel' type.
    # This is the same object as 'sentinel'.

    bint PySentinel_Check(object o)
    # Return true if o is a sentinel object.
    # The sentinel type does not allow subclasses, so this check is exact.

    object PySentinel_New(const char *name, const char *module_name)
    # Return value: New reference.
    # Return a new sentinel object with __name__ set to name and __module__ set to module_name.
    # name must not be NULL. If module_name is NULL, __module__ is set to None.
