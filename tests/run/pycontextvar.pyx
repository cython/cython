# mode: run

from cpython.contextvars cimport (
    PyContextVar_New, PyContextVar_New_with_default,
    get_value, get_value_no_default,
)

NOTHING = object()
CVAR = PyContextVar_New("cvar", NULL)
CVAR_WITH_DEFAULT = PyContextVar_New_with_default("cvar_wd", "DEFAULT")


import contextvars
PYCVAR = contextvars.ContextVar("pycvar")


def test_get_value(var, default=NOTHING):
    """
    >>> test_get_value(CVAR)
    >>> test_get_value(CVAR, "default")
    'default'
    >>> test_get_value(PYCVAR)
    >>> test_get_value(PYCVAR, "default")
    'default'
    >>> test_get_value(CVAR_WITH_DEFAULT)
    'DEFAULT'
    >>> test_get_value(CVAR_WITH_DEFAULT, "default")
    'DEFAULT'
    """
    return get_value(var, default) if default is not NOTHING else get_value(var)


def test_get_value_no_default(var, default=NOTHING):
    """
    >>> test_get_value_no_default(CVAR)
    >>> test_get_value_no_default(CVAR, "default")
    'default'
    >>> test_get_value_no_default(PYCVAR)
    >>> test_get_value_no_default(PYCVAR, "default")
    'default'
    >>> test_get_value_no_default(CVAR_WITH_DEFAULT)
    >>> test_get_value_no_default(CVAR_WITH_DEFAULT, "default")
    'default'
    """
    return get_value_no_default(var, default) if default is not NOTHING else get_value_no_default(var)
