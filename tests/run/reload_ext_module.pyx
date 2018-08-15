# mode: run
# tag: pep489


import reload_ext_module


def test_reload(module):
    """
    >>> module = test_reload(reload_ext_module)
    >>> module is reload_ext_module  # Py_mod_create enforces a singleton.
    True
    """
    return reload(module)
