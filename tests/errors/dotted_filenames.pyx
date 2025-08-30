# mode: compile
# tag: warnings
from dotted.module cimport bar


_WARNINGS = """
3:0: Dotted filenames ('dotted.module.pxd') are deprecated. Please use the normal Python package directory layout.
"""
