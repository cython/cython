from .object cimport PyObject

cdef extern from "Python.h":

    ###########################################################################
    # Context Variables Objects
    ###########################################################################

    bint PyContext_CheckExact(object o)
    bint PyContextVar_CheckExact(object o)
    bint PyContextToken_CheckExact(object o)

    object PyContext_New()
    # Return value: New reference.
    # Create a new empty context object. Returns NULL if an error has occurred.

    object PyContext_Copy(object ctx)
    # Return value: New reference.
    # Create a shallow copy of the passed ctx context object. Returns NULL if
    # an error has occurred.

    object PyContext_CopyCurrent()
    # Return value: New reference.
    # Create a shallow copy of the current thread context. Returns NULL if an
    # error has occurred.

    int PyContext_Enter(object ctx)
    # Set ctx as the current context for the current thread. Returns 0 on
    # success, and -1 on error.

    int PyContext_Exit(object ctx)
    # Deactivate the ctx context and restore the previous context as the
    # current context for the current thread. Returns 0 on success, and -1 on
    # error.

    int PyContext_ClearFreeList()
    # Clear the context variable free list. Return the total number of freed
    # items. This function always succeeds.

    object PyContextVar_New(const char *name, object def)
    # Return value: New reference.
    # Create a new ContextVar object. The name parameter is used for
    # introspection and debug purposes. The def parameter may optionally
    # specify the default value for the context variable. If an error has
    # occurred, this function returns NULL.

    int PyContextVar_Get(object var, object default_value, PyObject **value)
    # Get the value of a context variable. Returns -1 if an error has occurred
    # during lookup, and 0 if no error occurred, whether or not a value was
    # found. If the context variable was found, value will be a pointer to it.
    # If the context variable was not found, value will point to default_value
    # (if not NULL), the default value of var (if not NULL), or NULL.
    # If the value was found, the function will create a new reference to it.

    object PyContextVar_Set(object var, object value)
    # Return value: New reference.
    # Set the value of var to value in the current context. Returns a pointer
    # to a PyObject object, or NULL if an error has occurred.

    int PyContextVar_Reset(object var, object token)
    # Reset the state of the var context variable to that it was in before
    # PyContextVar_Set() was called. This function returns 0 on success and
    # -1 on error.
