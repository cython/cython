# mode: run
# tag: fused,
# tag: pure3.7

#cython: annotation_typing=True

from __future__ import annotations

import cython

class TestCls:
    def func1(self, arg: NotInPy):
        """
        >>> TestCls().func1(1.0)
        'float'
        >>> TestCls().func1(2)
        'int'
        """
        return cython.typeof(arg)

    if cython.compiled:
        @cython.locals(arg = NotInPy)  # NameError in pure Python
        def func2(self, arg):
            """
            >>> TestCls().func2(1.0)
            'float'
            >>> TestCls().func2(2)
            'int'
            """
            return cython.typeof(arg)

    def cpfunc(self, arg):
        """
        >>> TestCls().cpfunc(1.0)
        'float'
        >>> TestCls().cpfunc(2)
        'int'
        """
        return cython.typeof(arg)
