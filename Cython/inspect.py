from inspect import isfunction as orig_isfunction


def isfunction(obj):
    """
    Check if the given object is a user-defined Python function or a Cython function.

    This function extends the functionality of `inspect.isfunction` by also identifying
    Cython functions.
    """
    return orig_isfunction(obj) or type(obj).__name__ == "cython_function_or_method"
