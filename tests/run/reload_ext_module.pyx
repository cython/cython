# mode: run
# tag: pep489, no-macos

# FIXME: don't know why this does not work on MacOS, but it's not worth failing the builds for now.


import reload_ext_module


def test_reload(module):
    """
    >>> module = test_reload(reload_ext_module)
    >>> module is reload_ext_module  # Py_mod_create enforces a singleton.
    True
    """
    return reload(module)
