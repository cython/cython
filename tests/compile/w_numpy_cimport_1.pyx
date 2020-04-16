# mode: compile
# tag: warnings, numpy

cimport numpy as np
# np.import_array not called - should generate warning

_WARNINGS = """
1:0: 'numpy' cimported but 'numpy.import_array' was not called. Using Numpy through a cimport without calling 'import_array' may lead to crashes.
"""
