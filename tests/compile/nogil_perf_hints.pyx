# mode: compile
# tag: perf_hints

# Compile only to avoid needing to compile definitions of the functions
# declared in another pxd file

from nogil_perf_hints_pxd cimport f_has_except_value, f_missing_except_value, f_noexcept

def test():
    with nogil:
        # should not generate performance hints
        f_has_except_value()
        f_noexcept()
        # should generate performance hints.
        # (Unfortunately it's difficult to check the extra information on the 2nd+ line of the hint)
        f_missing_except_value()

_PERFORMANCE_HINTS = """
16:30: Exception check after calling 'f_missing_except_value' will always require the GIL to be acquired.
"""
