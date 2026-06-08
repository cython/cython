# mode: run
# tag: typing, final

# Attribute form: `import typing; @typing.final` on a cdef class.

import typing


@typing.final
cdef class FinalClass:
    """
    >>> f = FinalClass()
    >>> try:
    ...     class SubType(FinalClass): pass
    ... except TypeError:
    ...     print('PASSED!')
    PASSED!
    """
