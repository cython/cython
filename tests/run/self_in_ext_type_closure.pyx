# mode: run
# ticket: t742

import cython

@cython.cclass
class ExtType(object):
    def const1(self):
        return 1

    def ext_method0(self):
        """
        >>> x = ExtType()
        >>> x.ext_method0()()
        1
        """
        def func():
            return self.const1()
        return func

    def ext_method1(self, a):
        """
        >>> x = ExtType()
        >>> x.ext_method1(2)()
        (1, 2)
        """
        def func():
            return self.const1(), a
        return func

    def ext_method1_def(self, a=2):
        """
        >>> x = ExtType()
        >>> x.ext_method1_def()()
        (1, 2)
        >>> x.ext_method1_def(3)()
        (1, 3)
        """
        def func():
            return self.const1(), a
        return func

    def ext_method_args(self, *args):
        """
        >>> x = ExtType()
        >>> x.ext_method_args(2)()
        (1, 2)
        """
        def func():
            return self.const1(), args[0]
        return func

    def ext_method_args_only(*args):
        """
        >>> x = ExtType()
        >>> x.ext_method_args_only(2)()
        (1, 2)
        """
        def func():
            return args[0].const1(), args[1]
        return func


@cython.cclass
class GenType(object):
    def const1(self):
        return 1

    def gen0(self):
        """
        >>> x = GenType()
        >>> tuple(x.gen0())
        (1, 2)
        """
        yield self.const1()
        yield 2

    def gen1(self, a):
        """
        >>> x = GenType()
        >>> tuple(x.gen1(2))
        (1, 2)
        """
        yield self.const1()
        yield a

    def gen_default(self, a=2):
        """
        >>> x = GenType()
        >>> tuple(x.gen_default())
        (1, 2)
        >>> tuple(x.gen_default(3))
        (1, 3)
        """
        yield self.const1()
        yield a
