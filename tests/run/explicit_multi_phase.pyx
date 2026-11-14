# mode: run

# distutils: define_macros=CYTHON_PEP489_MULTI_PHASE_INIT=2 PyModuleDef_Slot=THIS_WONT_WORK

# This is really just a test that we can force it not to use PEP793 initialization.

some_global = 1

def basic_function():
    """
    basic_function()
    1
    """
    return some_global

def sanity_check_contents():
    """
    >>> sanity_check_contents()
    """
    import ctypes
    so_obj = ctypes.CDLL(__file__)  # exists
    so_obj.PyInit_explicit_multi_phase
    try:
        so_obj.PyModExport_explicit_multi_phase
    except AttributeError:
        pass  # good - it doesn't exist
    else:
        raise RuntimeError("PyModExport_explicit_multi_phase found") 