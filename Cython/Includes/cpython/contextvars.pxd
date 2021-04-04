from cpython.object cimport PyObject

cdef extern from "Python.h":

    ############################################################################
    # Context Variables Objects
    ############################################################################

    # PyContext
    # The C structure used to represent a `contextvars.Context` object.

    # PyContextVar
    # The C structure used to represent a `contextvars.ContextVar` object.

    # PyContextToken
    # The C structure used to represent a `contextvars.Token` object.

    # PyTypeObject PyContext_Type
    # Type object representing the `contextvars.Context` type.

    # PyTypeObject PyContextVar_Type
    # Type object representing the `contextvars.ContextVar` type.

    # PyTypeObject PyContextToken_Type
    # Type object representing the `contextvars.Token` type.

    bint PyContext_CheckExact(object obj)
    # Return `true` if `obj` is of type `PyContext_Type`.
    # `obj` must not be NULL. This function always succeeds.

    bint PyContextVar_CheckExact(object obj)
    # Return `true` if `obj` is of type `PyContextVar_Type`.
    # `obj` must not be NULL. This function always succeeds.

    bint PyContextToken_CheckExact(object obj)
    # Return `true` if `obj` is of type `PyContextToken_Type`.
    # `obj` must not be NULL. This function always succeeds.

    object PyContext_New()
    # Return value: New reference.
    # Create a new empty context object.
    # Returns NULL if an error has occurred.

    object PyContext_Copy(object ctx)
    # Return value: New reference.
    # Create a shallow copy of the passed `ctx` context object.
    # Returns NULL if an error has occurred.

    object PyContext_CopyCurrent()
    # Return value: New reference.
    # Create a shallow copy of the current thread context.
    # Returns NULL if an error has occurred.

    int PyContext_Enter(object ctx) except -1
    # Set `ctx` as the current context for the current thread.
    # Returns 0 on success, and -1 on error.

    int PyContext_Exit(object ctx) except -1
    # Deactivate the `ctx` context and restore the previous context
    # as the current context for the current thread.
    # Returns 0 on success, and -1 on error.

    object PyContextVar_New(const char* name, object default_value)
    # Return value: New reference.
    # Create a new ContextVar object. The `name` parameter is used
    # for introspection and debug purposes. The `default_value` parameter
    # may optionally specify the default value for the context variable.
    # If an error has occurred, this function returns NULL.

    int PyContextVar_Get1 "PyContextVar_Get" (PyObject* var, PyObject* default_value, PyObject** value) except -1
    # Get the value of a context variable.
    # Returns -1 if an error has occurred during lookup, and 0 if no error
    # occurred, whether or not a value was found.
    #
    # If the context variable was found, `value` will be a pointer to it.
    # If the context variable was not found, `value` will point to:
    #
    #   • `default_value`, if not NULL;
    #   • the default value of `var`, if not NULL;
    #   • NULL
    int PyContextVar_Get2 "PyContextVar_Get" (object var, object default_value, PyObject** value) except -1
    # a different declaration of PyContextVar_Get that requires default values
    # be passed on call.

    object PyContextVar_Set(object var, object value)
    # Return value: New reference.
    # Set the value of `var` to `value` in the current context.
    # Returns a pointer to a PyObject object, or NULL if an error has occurred.

    int PyContextVar_Reset(object var, object token) except -1
    # Reset the state of the `var` context variable to that it was in
    # before `PyContextVar_Set()` that returned `token` was called.
    # This function returns 0 on success and -1 on error.
