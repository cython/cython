# mode: compile
# tag: warnings, numpy

cimport numpy as np
np.import_array()
# np.import_array is called - no warning necessary

_WARNINGS = """
"""
