# mode: run

def call_with_builtin_exception(Exception e):
    """
    >>> call_with_builtin_exception(5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...

    >>> call_with_builtin_exception(Exception("xxx"))
    OK

    Subtypes are also OK
    >>> call_with_builtin_exception(RuntimeError("xxx"))
    OK
    """
    print("OK")

def call_with_builtin_base_exception(BaseException e):
    """
    >>> call_with_builtin_base_exception(5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...

    # Subtypes are also OK
    >>> call_with_builtin_base_exception(Exception("xxx"))
    OK

    >>> call_with_builtin_base_exception(BaseException("xxx"))
    OK
    """
    print("OK")


def builtin_exception_var_annotation(o):
    """
    >>> builtin_exception_var_annotation(5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...

    >>> builtin_exception_var_annotation(Exception())
    Good

    subtypes OK
    >>> builtin_exception_var_annotation(ValueError())
    Good
    """
    v: Exception = o
    print("Good")

def builtin_base_exception_var_annotation(o):
    """
    >>> builtin_base_exception_var_annotation(5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...

    subtypes ok
    >>> builtin_base_exception_var_annotation(Exception())
    Good

    >>> builtin_base_exception_var_annotation(BaseException())
    Good
    """
    v: BaseException = o
    print("Good")
