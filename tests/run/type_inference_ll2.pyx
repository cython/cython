# cython: infer_types = True
# cython: language_level=2

"""
Type inference tests with 'language_level=2'.
"""

def check_language_level():
    """
    >>> check_language_level()
    2
    """
    return 3 if IS_LANGUAGE_LEVEL_3 else 2


include "type_inference.pyx"
