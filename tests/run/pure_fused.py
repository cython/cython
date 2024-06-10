# mode: run
# tag: fused, pure3.6

#cython: annotation_typing=True

import cython
from typing import Union

InPy = cython.fused_type(cython.int, cython.float)

class TestCls:
    # although annotations as strings isn't recommended and generates a warning
    # it does allow the test to run on more (pure) Python versions
    def func1(self, arg: 'NotInPy'):
        """
        >>> TestCls().func1(1.0)
        'float'
        >>> TestCls().func1(2)
        'int'
        """
        loc: 'NotInPy' = arg
        return cython.typeof(arg)

    if cython.compiled:
        @cython.locals(arg=NotInPy, loc=NotInPy)  # NameError for 'NotInPy' in pure Python
        def func2(self, arg):
            """
            >>> TestCls().func2(1.0)
            'float'
            >>> TestCls().func2(2)
            'int'
            """
            loc = arg
            return cython.typeof(arg)

    def cpfunc(self, arg):
        """
        >>> TestCls().cpfunc(1.0)
        'float'
        >>> TestCls().cpfunc(2)
        'int'
        """
        loc = arg
        return cython.typeof(arg)

    def func1_inpy(self, arg: InPy):
        """
        >>> TestCls().func1_inpy(1.0)
        'float'
        >>> TestCls().func1_inpy(2)
        'int'
        """
        loc: InPy = arg
        return cython.typeof(arg)

    @cython.locals(arg = InPy, loc = InPy)
    def func2_inpy(self, arg):
        """
        >>> TestCls().func2_inpy(1.0)
        'float'
        >>> TestCls().func2_inpy(2)
        'int'
        """
        loc = arg
        return cython.typeof(arg)

@cython.cfunc
def _union(arg1: Union[cython.int, str], arg2: Union[cython.int, str]):
    return cython.typeof(arg1), cython.typeof(arg2)

@cython.cfunc
def return_union(t: cython.int) -> Union[cython.int, cython.float]:
    if t == 1:
        return 2
    else:
        return 1.0

class TestUnion:

    def annotation(self, arg: Union[cython.int, cython.float]):
        """
        >>> TestUnion().annotation(1.0)
        'float'
        >>> TestUnion().annotation(2)
        'int'
        """
        return cython.typeof(arg)

    if cython.compiled:
        def annotation_return(self, arg):
            """
            >>> TestUnion().annotation_return(1)
            (2, 'Python object')
            >>> TestUnion().annotation_return(2)
            (1.0, 'Python object')
            """
            ret = return_union(arg)
            return ret, cython.typeof(ret)
    else:
        def annotation_return(self, arg):
            """
            >>> TestUnion().annotation_return(1)
            (2, 'int')
            >>> TestUnion().annotation_return(2)
            (1.0, 'float')
            """
            ret = return_union(arg)
            return ret, cython.typeof(ret)

    if cython.compiled:
        def annotation_multiple_args(self, arg1: Union[cython.int, str], arg2: Union[cython.int, str]):
            """
            >>> TestUnion().annotation_multiple_args(5, 'mystr')
            ('int', 'str object')
            >>> TestUnion().annotation_multiple_args('mystr', 3)
            ('str object', 'int')
            """
            return _union(arg1, arg2)
