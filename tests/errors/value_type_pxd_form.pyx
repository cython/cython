# mode: error
# Tests that a value_type declared in a genuine hand-written .pxd (not via
# --cimport-from-pyx) produces a clean compile error.  The consumer imports
# from value_type_pxd_form_helper.pxd which declares Vec2 with @value_type.
from value_type_pxd_form_helper cimport Vec2

_ERRORS = """
value_type_pxd_form_helper.pxd:7:0: value_type classes cannot be declared in a hand-written .pxd file (cross-module value types require '--cimport-from-pyx')
"""
