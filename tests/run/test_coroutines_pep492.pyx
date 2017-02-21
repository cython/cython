# cython: language_level=3, binding=True
# mode: run
# tag: pep492, asyncfor, await

import re
import gc
import sys
import copy
#import types
import pickle
import os.path
#import inspect
import unittest
import warnings
import contextlib

from Cython.Compiler import Errors


try:
    from types import coroutine as types_coroutine
except ImportError:
    # duck typed types.coroutine() decorator copied from types.py in Py3.5
    class types_coroutine(object):
        def __init__(self, gen):
            self._gen = gen

        class _GeneratorWrapper(object):
            def __init__(self, gen):
                self.__wrapped__ = gen
                self.send = gen.send
                self.throw = gen.throw
                self.close = gen.close
                self.__name__ = getattr(gen, '__name__', None)
                self.__qualname__ = getattr(gen, '__qualname__', None)
            @property
            def gi_code(self):
                return self.__wrapped__.gi_code
            @property
            def gi_frame(self):
                return self.__wrapped__.gi_frame
            @property
            def gi_running(self):
                return self.__wrapped__.gi_running
            cr_code = gi_code
            cr_frame = gi_frame
            cr_running = gi_running
            def __next__(self):
                return next(self.__wrapped__)
            def __iter__(self):
                return self.__wrapped__
            __await__ = __iter__

        def __call__(self, *args, **kwargs):
            return self._GeneratorWrapper(self._gen(*args, **kwargs))


# compiled exec()
def exec(code_string, l, g):
    from Cython.Shadow import inline
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    old_stderr = sys.stderr
    try:
        sys.stderr = StringIO()
        ns = inline(code_string, locals=l, globals=g, lib_dir=os.path.dirname(__file__))
    finally:
        sys.stderr = old_stderr
    g.update(ns)


class AsyncYieldFrom(object):
    def __init__(self, obj):
        self.obj = obj

    def __await__(self):
        yield from self.obj


class AsyncYield(object):
    def __init__(self, value):
        self.value = value

    def __await__(self):
        yield self.value


def run_async(coro):
    #assert coro.__class__ is types.GeneratorType
    assert coro.__class__.__name__ in ('coroutine', '_GeneratorWrapper'), coro.__class__.__name__

    buffer = []
    result = None
    while True:
        try:
            buffer.append(coro.send(None))
        except StopIteration as ex:
            result = ex.value if sys.version_info >= (3, 5) else ex.args[0] if ex.args else None
            break
    return buffer, result


def run_async__await__(coro):
    assert coro.__class__.__name__ in ('coroutine', '_GeneratorWrapper'), coro.__class__.__name__
    aw = coro.__await__()
    buffer = []
    result = None
    i = 0
    while True:
        try:
            if i % 2:
                buffer.append(next(aw))
            else:
                buffer.append(aw.send(None))
            i += 1
        except StopIteration as ex:
            result = ex.value if sys.version_info >= (3, 5) else ex.args[0] if ex.args else None
            break
    return buffer, result


@contextlib.contextmanager
def silence_coro_gc():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield
        gc.collect()


def min_py27(method):
    return None if sys.version_info < (2, 7) else method


def ignore_py26(manager):
    @contextlib.contextmanager
    def dummy():
        yield
    return dummy() if sys.version_info < (2, 7) else manager


class AsyncBadSyntaxTest(unittest.TestCase):

    @contextlib.contextmanager
    def assertRaisesRegex(self, exc_type, regex):
        # the error messages usually don't match, so we just ignore them
        try:
            yield
        except exc_type:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_badsyntax_9(self):
        ns = {}
        for comp in {'(await a for a in b)',
                     '[await a for a in b]',
                     '{await a for a in b}',
                     '{await a: a for a in b}'}:

            with self.assertRaisesRegex(Errors.CompileError, 'await.*in comprehen'):
                exec('async def f():\n\t{0}'.format(comp), ns, ns)

    def test_badsyntax_10(self):
        # Tests for issue 24619

        samples = [
            """async def foo():
                   def bar(): pass
                   await = 1
            """,

            """async def foo():

                   def bar(): pass
                   await = 1
            """,

            """async def foo():
                   def bar(): pass
                   if 1:
                       await = 1
            """,

            """def foo():
                   async def bar(): pass
                   if 1:
                       await a
            """,

            """def foo():
                   async def bar(): pass
                   await a
            """,

            """def foo():
                   def baz(): pass
                   async def bar(): pass
                   await a
            """,

            """def foo():
                   def baz(): pass
                   # 456
                   async def bar(): pass
                   # 123
                   await a
            """,

            """async def foo():
                   def baz(): pass
                   # 456
                   async def bar(): pass
                   # 123
                   await = 2
            """,

            """def foo():

                   def baz(): pass

                   async def bar(): pass

                   await a
            """,

            """async def foo():

                   def baz(): pass

                   async def bar(): pass

                   await = 2
            """,

            """async def foo():
                   def async(): pass
            """,

            """async def foo():
                   def await(): pass
            """,

            """async def foo():
                   def bar():
                       await
            """,

            """async def foo():
                   return lambda async: await
            """,

            """async def foo():
                   return lambda a: await
            """,

            """await a()""",

            """async def foo(a=await b):
                   pass
            """,

            """async def foo(a:await b):
                   pass
            """,

            """def baz():
                   async def foo(a=await b):
                       pass
            """,

            """async def foo(async):
                   pass
            """,

            """async def foo():
                   def bar():
                        def baz():
                            async = 1
            """,

            """async def foo():
                   def bar():
                        def baz():
                            pass
                        async = 1
            """,

            """def foo():
                   async def bar():

                        async def baz():
                            pass

                        def baz():
                            42

                        async = 1
            """,

            """async def foo():
                   def bar():
                        def baz():
                            pass\nawait foo()
            """,

            """def foo():
                   def bar():
                        async def baz():
                            pass\nawait foo()
            """,

            """async def foo(await):
                   pass
            """,

            """def foo():

                   async def bar(): pass

                   await a
            """,

            """def foo():
                   async def bar():
                        pass\nawait a
            """]

        for code in samples:
            # assertRaises() differs in Py2.6, so use our own assertRaisesRegex() instead
            with self.subTest(code=code), self.assertRaisesRegex(Errors.CompileError, '.'):
                exec(code, {}, {})

    if not hasattr(unittest.TestCase, 'subTest'):
        @contextlib.contextmanager
        def subTest(self, code, **kwargs):
            try:
                yield
            except Exception:
                print(code)
                raise

    def test_goodsyntax_1(self):
        # Tests for issue 24619

        def foo(await):
            async def foo(): pass
            async def foo():
                pass
            return await + 1
        self.assertEqual(foo(10), 11)

        def foo(await):
            async def foo(): pass
            async def foo(): pass
            return await + 2
        self.assertEqual(foo(20), 22)

        def foo(await):

            async def foo(): pass

            async def foo(): pass

            return await + 2
        self.assertEqual(foo(20), 22)

        def foo(await):
            """spam"""
            async def foo(): \
                pass
            # 123
            async def foo(): pass
            # 456
            return await + 2
        self.assertEqual(foo(20), 22)

        def foo(await):
            def foo(): pass
            def foo(): pass
            async def bar(): return await_
            await_ = await
            try:
                bar().send(None)
            except StopIteration as ex:
                return ex.args[0]
        self.assertEqual(foo(42), 42)

        async def f(z):
            async def g(): pass
            await z
        await = 1
        #self.assertTrue(inspect.iscoroutinefunction(f))


class TokenizerRegrTest(unittest.TestCase):

    def test_oneline_defs(self):
        buf = []
        for i in range(500):
            buf.append('def i{i}(): return {i}'.format(i=i))
        buf = '\n'.join(buf)

        # Test that 500 consequent, one-line defs is OK
        ns = {}
        exec(buf, ns, ns)
        self.assertEqual(ns['i499'](), 499)

        # Test that 500 consequent, one-line defs *and*
        # one 'async def' following them is OK
        buf += '\nasync def foo():\n    return'
        ns = {}
        exec(buf, ns, ns)
        self.assertEqual(ns['i499'](), 499)
        self.assertEqual(type(ns['foo']()).__name__, 'coroutine')
        #self.assertTrue(inspect.iscoroutinefunction(ns['foo']))


class CoroutineTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # never mark warnings as "already seen" to prevent them from being suppressed
        from warnings import simplefilter
        simplefilter("always")

    @contextlib.contextmanager
    def assertRaises(self, exc_type):
        try:
            yield
        except exc_type:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    @contextlib.contextmanager
    def assertRaisesRegex(self, exc_type, regex):
        # the error messages usually don't match, so we just ignore them
        try:
            yield
        except exc_type:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    @contextlib.contextmanager
    def assertWarnsRegex(self, exc_type, regex):
        from warnings import catch_warnings
        with catch_warnings(record=True) as log:
            yield

        first_match = None
        for warning in log:
            w = warning.message
            if not isinstance(w, exc_type):
                continue
            if first_match is None:
                first_match = w
            if re.search(regex, str(w)):
                self.assertTrue(True)
                return

        if first_match is None:
            self.assertTrue(False, "no warning was raised of type '%s'" % exc_type.__name__)
        else:
            self.assertTrue(False, "'%s' did not match '%s'" % (first_match, regex))

    if not hasattr(unittest.TestCase, 'assertRegex'):
        def assertRegex(self, value, regex):
            self.assertTrue(re.search(regex, str(value)),
                            "'%s' did not match '%s'" % (value, regex))

    if not hasattr(unittest.TestCase, 'assertIn'):
        def assertIn(self, member, container, msg=None):
            self.assertTrue(member in container, msg)

    if not hasattr(unittest.TestCase, 'assertIsNone'):
        def assertIsNone(self, value, msg=None):
            self.assertTrue(value is None, msg)

    if not hasattr(unittest.TestCase, 'assertIsNotNone'):
        def assertIsNotNone(self, value, msg=None):
            self.assertTrue(value is not None, msg)

    def test_gen_1(self):
        def gen(): yield
        self.assertFalse(hasattr(gen, '__await__'))

    def test_func_attributes(self):
        async def foo():
            return 10

        f = foo()
        self.assertEqual(f.__name__, 'foo')
        self.assertEqual(f.__qualname__, 'CoroutineTest.test_func_attributes.<locals>.foo')
        self.assertEqual(f.__module__, 'test_coroutines_pep492')

    def test_func_1(self):
        async def foo():
            return 10

        f = foo()
        self.assertEqual(f.__class__.__name__, 'coroutine')
        #self.assertIsInstance(f, types.CoroutineType)
        #self.assertTrue(bool(foo.__code__.co_flags & 0x80))
        #self.assertTrue(bool(foo.__code__.co_flags & 0x20))
        #self.assertTrue(bool(f.cr_code.co_flags & 0x80))
        #self.assertTrue(bool(f.cr_code.co_flags & 0x20))
        self.assertEqual(run_async(f), ([], 10))

        self.assertEqual(run_async__await__(foo()), ([], 10))

        def bar(): pass
        self.assertFalse(bool(bar.__code__.co_flags & 0x80))

    # TODO
    def __test_func_2(self):
        async def foo():
            raise StopIteration

        with self.assertRaisesRegex(
                RuntimeError, "coroutine raised StopIteration"):

            run_async(foo())

    def test_func_3(self):
        async def foo():
            raise StopIteration

        with silence_coro_gc():
            self.assertRegex(repr(foo()), '^<coroutine object.* at 0x.*>$')

    def test_func_4(self):
        async def foo():
            raise StopIteration

        check = lambda: self.assertRaisesRegex(
            TypeError, "'coroutine' object is not iterable")

        with check():
            list(foo())

        with check():
            tuple(foo())

        with check():
            sum(foo())

        with check():
            iter(foo())

        with check():
            next(foo())

        with silence_coro_gc(), check():
            for i in foo():
                pass

        with silence_coro_gc(), check():
            [i for i in foo()]

    def test_func_5(self):
        @types_coroutine
        def bar():
            yield 1

        async def foo():
            await bar()

        check = lambda: self.assertRaisesRegex(
            TypeError, "'coroutine' object is not iterable")

        with check():
            for el in foo(): pass

        # the following should pass without an error
        for el in bar():
            self.assertEqual(el, 1)
        self.assertEqual([el for el in bar()], [1])
        self.assertEqual(tuple(bar()), (1,))
        self.assertEqual(next(iter(bar())), 1)

    def test_func_6(self):
        @types_coroutine
        def bar():
            yield 1
            yield 2

        async def foo():
            await bar()

        f = foo()
        self.assertEqual(f.send(None), 1)
        self.assertEqual(f.send(None), 2)
        with self.assertRaises(StopIteration):
            f.send(None)

    # TODO (or not? see test_func_8() below)
    def __test_func_7(self):
        async def bar():
            return 10

        def foo():
            yield from bar()

        with silence_coro_gc(), self.assertRaisesRegex(
            TypeError,
            "cannot 'yield from' a coroutine object in a non-coroutine generator"):

            list(foo())

    def test_func_8(self):
        @types_coroutine
        def bar():
            return (yield from foo())

        async def foo():
            return 'spam'

        self.assertEqual(run_async(bar()), ([], 'spam') )

    def test_func_9(self):
        async def foo(): pass

        with self.assertWarnsRegex(
            RuntimeWarning, "coroutine '.*test_func_9.*foo' was never awaited"):

            foo()
            gc.collect()

    def test_func_10(self):
        N = 0

        @types_coroutine
        def gen():
            nonlocal N
            try:
                a = yield
                yield (a ** 2)
            except ZeroDivisionError:
                N += 100
                raise
            finally:
                N += 1

        async def foo():
            await gen()

        coro = foo()
        aw = coro.__await__()
        self.assertTrue(aw is iter(aw))
        next(aw)
        self.assertEqual(aw.send(10), 100)
        with self.assertRaises(TypeError):
            type(aw).send(None, None)

        self.assertEqual(N, 0)
        aw.close()
        self.assertEqual(N, 1)
        with self.assertRaises(TypeError):   # removed from CPython test suite?
            type(aw).close(None)

        coro = foo()
        aw = coro.__await__()
        next(aw)
        with self.assertRaises(ZeroDivisionError):
            aw.throw(ZeroDivisionError, None, None)
        self.assertEqual(N, 102)
        with self.assertRaises(TypeError):   # removed from CPython test suite?
            type(aw).throw(None, None, None, None)

    def test_func_11(self):
        async def func(): pass
        coro = func()
        # Test that PyCoro_Type and _PyCoroWrapper_Type types were properly
        # initialized
        self.assertIn('__await__', dir(coro))
        self.assertIn('__iter__', dir(coro.__await__()))
        self.assertIn('coroutine_wrapper', repr(coro.__await__()))
        coro.close() # avoid RuntimeWarning

    def test_func_12(self):
        async def g():
            i = me.send(None)
            await None
        me = g()
        with self.assertRaisesRegex(ValueError,
                                    "coroutine already executing"):
            me.send(None)

    def test_func_13(self):
        async def g():
            pass
        with self.assertRaisesRegex(
            TypeError,
            "can't send non-None value to a just-started coroutine"):

            g().send('spam')

    def test_func_14(self):
        @types_coroutine
        def gen():
            yield
        async def coro():
            try:
                await gen()
            except GeneratorExit:
                await gen()
        c = coro()
        c.send(None)
        with self.assertRaisesRegex(RuntimeError,
                                    "coroutine ignored GeneratorExit"):
            c.close()

    def test_cr_await(self):
        @types_coroutine
        def a():
            #self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_RUNNING)
            self.assertIsNone(coro_b.cr_await)
            yield
            #self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_RUNNING)
            # FIXME: no idea why the following works in CPython:
            #self.assertIsNone(coro_b.cr_await)

        async def c():
            await a()

        async def b():
            self.assertIsNone(coro_b.cr_await)
            await c()
            self.assertIsNone(coro_b.cr_await)

        coro_b = b()
        #self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_CREATED)
        self.assertIsNone(coro_b.cr_await)

        coro_b.send(None)
        #self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_SUSPENDED)
        #self.assertEqual(coro_b.cr_await.cr_await.gi_code.co_name, 'a')
        self.assertIsNotNone(coro_b.cr_await.cr_await)
        self.assertEqual(coro_b.cr_await.cr_await.__name__, 'a')

        with self.assertRaises(StopIteration):
            coro_b.send(None)  # complete coroutine
        #self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_CLOSED)
        self.assertIsNone(coro_b.cr_await)

    def test_corotype_1(self):
        async def f(): pass
        ct = type(f())
        self.assertIn('into coroutine', ct.send.__doc__)
        self.assertIn('inside coroutine', ct.close.__doc__)
        self.assertIn('in coroutine', ct.throw.__doc__)
        self.assertIn('of the coroutine', ct.__dict__['__name__'].__doc__)
        self.assertIn('of the coroutine', ct.__dict__['__qualname__'].__doc__)
        self.assertEqual(ct.__name__, 'coroutine')

        async def f(): pass
        c = f()
        self.assertIn('coroutine object', repr(c))
        c.close()

    def test_await_1(self):

        async def foo():
            await 1
        with self.assertRaisesRegex(TypeError, "object int can.t.*await"):
            run_async(foo())

    def test_await_2(self):
        async def foo():
            await []
        with self.assertRaisesRegex(TypeError, "object list can.t.*await"):
            run_async(foo())

    def test_await_3(self):
        async def foo():
            await AsyncYieldFrom([1, 2, 3])

        self.assertEqual(run_async(foo()), ([1, 2, 3], None))
        self.assertEqual(run_async__await__(foo()), ([1, 2, 3], None))

    def test_await_4(self):
        async def bar():
            return 42

        async def foo():
            return await bar()

        self.assertEqual(run_async(foo()), ([], 42))

    def test_await_5(self):
        class Awaitable(object):
            def __await__(self):
                return

        async def foo():
            return (await Awaitable())

        with self.assertRaisesRegex(
            TypeError, "__await__.*returned non-iterator of type"):

            run_async(foo())

    def test_await_6(self):
        class Awaitable(object):
            def __await__(self):
                return iter([52])

        async def foo():
            return (await Awaitable())

        self.assertEqual(run_async(foo()), ([52], None))

    def test_await_7(self):
        class Awaitable(object):
            def __await__(self):
                yield 42
                return 100

        async def foo():
            return (await Awaitable())

        self.assertEqual(run_async(foo()), ([42], 100))

    def test_await_8(self):
        class Awaitable(object):
            pass

        async def foo(): return (await Awaitable())

        with self.assertRaisesRegex(
            TypeError, "object Awaitable can't be used in 'await' expression"):

            run_async(foo())

    def test_await_9(self):
        def wrap():
            return bar

        async def bar():
            return 42

        async def foo():
            b = bar()

            db = {'b':  lambda: wrap}

            class DB(object):
                b = staticmethod(wrap)

            return (await bar() + await wrap()() + await db['b']()()() +
                    await bar() * 1000 + await DB.b()())

        async def foo2():
            return -await bar()

        self.assertEqual(run_async(foo()), ([], 42168))
        self.assertEqual(run_async(foo2()), ([], -42))

    def test_await_10(self):
        async def baz():
            return 42

        async def bar():
            return baz()

        async def foo():
            return await (await bar())

        self.assertEqual(run_async(foo()), ([], 42))

    def test_await_11(self):
        def ident(val):
            return val

        async def bar():
            return 'spam'

        async def foo():
            return ident(val=await bar())

        async def foo2():
            return await bar(), 'ham'

        self.assertEqual(run_async(foo2()), ([], ('spam', 'ham')))

    def test_await_12(self):
        async def coro():
            return 'spam'

        class Awaitable(object):
            def __await__(self):
                return coro()

        async def foo():
            return await Awaitable()

        with self.assertRaisesRegex(
            TypeError, "__await__\(\) returned a coroutine"):

            run_async(foo())

    def test_await_13(self):
        class Awaitable(object):
            def __await__(self):
                return self

        async def foo():
            return await Awaitable()

        with self.assertRaisesRegex(
            TypeError, "__await__.*returned non-iterator of type"):

            run_async(foo())

    def test_await_14(self):
        class Wrapper(object):
            # Forces the interpreter to use CoroutineType.__await__
            def __init__(self, coro):
                self.coro = coro
            def __await__(self):
                return self.coro.__await__()

        class FutureLike(object):
            def __await__(self):
                return (yield)

        class Marker(Exception):
            pass

        async def coro1():
            try:
                return await FutureLike()
            except ZeroDivisionError:
                raise Marker
        async def coro2():
            return await Wrapper(coro1())

        c = coro2()
        c.send(None)
        with self.assertRaisesRegex(StopIteration, 'spam'):
            c.send('spam')

        c = coro2()
        c.send(None)
        with self.assertRaises(Marker):
            c.throw(ZeroDivisionError)

    def test_await_iterator(self):
        async def foo():
            return 123

        coro = foo()
        it = coro.__await__()
        self.assertEqual(type(it).__name__, 'coroutine_wrapper')

        with self.assertRaisesRegex(TypeError, "cannot instantiate 'coroutine_wrapper' type"):
            type(it)()  # cannot instantiate

        with self.assertRaisesRegex(StopIteration, "123"):
            next(it)

    def test_with_1(self):
        class Manager(object):
            def __init__(self, name):
                self.name = name

            async def __aenter__(self):
                await AsyncYieldFrom(['enter-1-' + self.name,
                                      'enter-2-' + self.name])
                return self

            async def __aexit__(self, *args):
                await AsyncYieldFrom(['exit-1-' + self.name,
                                      'exit-2-' + self.name])

                if self.name == 'B':
                    return True


        async def foo():
            async with Manager("A") as a, Manager("B") as b:
                await AsyncYieldFrom([('managers', a.name, b.name)])
                1/0

        f = foo()
        result, _ = run_async(f)

        self.assertEqual(
            result, ['enter-1-A', 'enter-2-A', 'enter-1-B', 'enter-2-B',
                     ('managers', 'A', 'B'),
                     'exit-1-B', 'exit-2-B', 'exit-1-A', 'exit-2-A']
        )

        async def foo():
            async with Manager("A") as a, Manager("C") as c:
                await AsyncYieldFrom([('managers', a.name, c.name)])
                1/0

        with self.assertRaises(ZeroDivisionError):
            run_async(foo())

    def test_with_2(self):
        class CM(object):
            def __aenter__(self):
                pass

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(AttributeError, '__aexit__'):
            run_async(foo())

    def test_with_3(self):
        class CM(object):
            def __aexit__(self):
                pass

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(AttributeError, '__aenter__'):
            run_async(foo())

    def test_with_4(self):
        class CM(object):
            def __enter__(self):
                pass

            def __exit__(self):
                pass

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(AttributeError, '__aexit__'):
            run_async(foo())

    def test_with_5(self):
        # While this test doesn't make a lot of sense,
        # it's a regression test for an early bug with opcodes
        # generation

        class CM(object):
            async def __aenter__(self):
                return self

            async def __aexit__(self, *exc):
                pass

        async def func():
            async with CM():
                assert (1, ) == 1

        with self.assertRaises(AssertionError):
            run_async(func())

    def test_with_6(self):
        class CM(object):
            def __aenter__(self):
                return 123

            def __aexit__(self, *e):
                return 456

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(
            TypeError, "object int can't be used in 'await' expression"):
            # it's important that __aexit__ wasn't called
            run_async(foo())

    def test_with_7(self):
        class CM(object):
            async def __aenter__(self):
                return self

            def __aexit__(self, *e):
                return 444

        async def foo():
            async with CM():
                1/0

        try:
            run_async(foo())
        except TypeError as exc:
            self.assertRegex(
                exc.args[0], "object int can't be used in 'await' expression")
            if sys.version_info[0] >= 3:
                self.assertTrue(exc.__context__ is not None)
                self.assertTrue(isinstance(exc.__context__, ZeroDivisionError))
        else:
            self.fail('invalid asynchronous context manager did not fail')


    def test_with_8(self):
        CNT = 0

        class CM(object):
            async def __aenter__(self):
                return self

            def __aexit__(self, *e):
                return 456

        async def foo():
            nonlocal CNT
            async with CM():
                CNT += 1


        with self.assertRaisesRegex(
            TypeError, "object int can't be used in 'await' expression"):

            run_async(foo())

        self.assertEqual(CNT, 1)

    def test_with_9(self):
        CNT = 0

        class CM(object):
            async def __aenter__(self):
                return self

            async def __aexit__(self, *e):
                1/0

        async def foo():
            nonlocal CNT
            async with CM():
                CNT += 1

        with self.assertRaises(ZeroDivisionError):
            run_async(foo())

        self.assertEqual(CNT, 1)

    def test_with_10(self):
        CNT = 0

        class CM(object):
            async def __aenter__(self):
                return self

            async def __aexit__(self, *e):
                1/0

        async def foo():
            nonlocal CNT
            async with CM():
                async with CM():
                    raise RuntimeError

        try:
            run_async(foo())
        except ZeroDivisionError as exc:
            pass  # FIXME!
            #if sys.version_info[0] >= 3:
            #    self.assertTrue(exc.__context__ is not None)
            #    self.assertTrue(isinstance(exc.__context__, ZeroDivisionError))
            #    self.assertTrue(isinstance(exc.__context__.__context__, RuntimeError))
        else:
            self.fail('exception from __aexit__ did not propagate')

    def test_with_11(self):
        CNT = 0

        class CM(object):
            async def __aenter__(self):
                raise NotImplementedError

            async def __aexit__(self, *e):
                1/0

        async def foo():
            nonlocal CNT
            async with CM():
                raise RuntimeError

        try:
            run_async(foo())
        except NotImplementedError as exc:
            if sys.version_info[0] >= 3:
                self.assertTrue(exc.__context__ is None)
        else:
            self.fail('exception from __aenter__ did not propagate')

    def test_with_12(self):
        CNT = 0

        class CM(object):
            async def __aenter__(self):
                return self

            async def __aexit__(self, *e):
                return True

        async def foo():
            nonlocal CNT
            async with CM() as cm:
                self.assertIs(cm.__class__, CM)
                raise RuntimeError

        run_async(foo())

    def test_with_13(self):
        CNT = 0

        class CM(object):
            async def __aenter__(self):
                1/0

            async def __aexit__(self, *e):
                return True

        async def foo():
            nonlocal CNT
            CNT += 1
            async with CM():
                CNT += 1000
            CNT += 10000

        with self.assertRaises(ZeroDivisionError):
            run_async(foo())
        self.assertEqual(CNT, 1)

    def test_for_1(self):
        aiter_calls = 0

        class AsyncIter(object):
            def __init__(self):
                self.i = 0

            async def __aiter__(self):
                nonlocal aiter_calls
                aiter_calls += 1
                return self

            async def __anext__(self):
                self.i += 1

                if not (self.i % 10):
                    await AsyncYield(self.i * 10)

                if self.i > 100:
                    raise StopAsyncIteration

                return self.i, self.i


        buffer = []
        async def test1():
            with ignore_py26(self.assertWarnsRegex(PendingDeprecationWarning, "legacy")):
                async for i1, i2 in AsyncIter():
                    buffer.append(i1 + i2)

        yielded, _ = run_async(test1())
        # Make sure that __aiter__ was called only once
        self.assertEqual(aiter_calls, 1)
        self.assertEqual(yielded, [i * 100 for i in range(1, 11)])
        self.assertEqual(buffer, [i*2 for i in range(1, 101)])


        buffer = []
        async def test2():
            nonlocal buffer
            with ignore_py26(self.assertWarnsRegex(PendingDeprecationWarning, "legacy")):
                async for i in AsyncIter():
                    buffer.append(i[0])
                    if i[0] == 20:
                        break
                else:
                    buffer.append('what?')
            buffer.append('end')

        yielded, _ = run_async(test2())
        # Make sure that __aiter__ was called only once
        self.assertEqual(aiter_calls, 2)
        self.assertEqual(yielded, [100, 200])
        self.assertEqual(buffer, [i for i in range(1, 21)] + ['end'])


        buffer = []
        async def test3():
            nonlocal buffer
            with ignore_py26(self.assertWarnsRegex(PendingDeprecationWarning, "legacy")):
                async for i in AsyncIter():
                    if i[0] > 20:
                        continue
                    buffer.append(i[0])
                else:
                    buffer.append('what?')
            buffer.append('end')

        yielded, _ = run_async(test3())
        # Make sure that __aiter__ was called only once
        self.assertEqual(aiter_calls, 3)
        self.assertEqual(yielded, [i * 100 for i in range(1, 11)])
        self.assertEqual(buffer, [i for i in range(1, 21)] +
                                 ['what?', 'end'])

    def test_for_2(self):
        tup = (1, 2, 3)
        refs_before = sys.getrefcount(tup)

        async def foo():
            async for i in tup:
                print('never going to happen')

        with self.assertRaisesRegex(
                TypeError, "async for' requires an object.*__aiter__.*tuple"):

            run_async(foo())

        self.assertEqual(sys.getrefcount(tup), refs_before)

    def test_for_3(self):
        class I(object):
            def __aiter__(self):
                return self

        aiter = I()
        refs_before = sys.getrefcount(aiter)

        async def foo():
            async for i in aiter:
                print('never going to happen')

        with self.assertRaisesRegex(
                TypeError,
                "async for' received an invalid object.*__aiter.*\: I"):

            run_async(foo())

        self.assertEqual(sys.getrefcount(aiter), refs_before)

    def test_for_4(self):
        class I(object):
            def __aiter__(self):
                return self

            def __anext__(self):
                return ()

        aiter = I()
        refs_before = sys.getrefcount(aiter)

        async def foo():
            async for i in aiter:
                print('never going to happen')

        with self.assertRaisesRegex(
                TypeError,
                "async for' received an invalid object.*__anext__.*tuple"):

            run_async(foo())

        self.assertEqual(sys.getrefcount(aiter), refs_before)

    def test_for_5(self):
        class I(object):
            async def __aiter__(self):
                return self

            def __anext__(self):
                return 123

        async def foo():
            with self.assertWarnsRegex(PendingDeprecationWarning, "legacy"):
                async for i in I():
                    print('never going to happen')

        with self.assertRaisesRegex(
                TypeError,
                "async for' received an invalid object.*__anext.*int"):

            run_async(foo())

    def test_for_6(self):
        I = 0

        class Manager(object):
            async def __aenter__(self):
                nonlocal I
                I += 10000

            async def __aexit__(self, *args):
                nonlocal I
                I += 100000

        class Iterable(object):
            def __init__(self):
                self.i = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.i > 10:
                    raise StopAsyncIteration
                self.i += 1
                return self.i

        ##############

        manager = Manager()
        iterable = Iterable()
        mrefs_before = sys.getrefcount(manager)
        irefs_before = sys.getrefcount(iterable)

        async def main():
            nonlocal I

            async with manager:
                async for i in iterable:
                    I += 1
            I += 1000

        run_async(main())
        self.assertEqual(I, 111011)

        self.assertEqual(sys.getrefcount(manager), mrefs_before)
        self.assertEqual(sys.getrefcount(iterable), irefs_before)

        ##############

        async def main():
            nonlocal I

            async with Manager():
                async for i in Iterable():
                    I += 1
            I += 1000

            async with Manager():
                async for i in Iterable():
                    I += 1
            I += 1000

        run_async(main())
        self.assertEqual(I, 333033)

        ##############

        async def main():
            nonlocal I

            async with Manager():
                I += 100
                async for i in Iterable():
                    I += 1
                else:
                    I += 10000000
            I += 1000

            async with Manager():
                I += 100
                async for i in Iterable():
                    I += 1
                else:
                    I += 10000000
            I += 1000

        run_async(main())
        self.assertEqual(I, 20555255)

    def test_for_7(self):
        CNT = 0
        class AI(object):
            async def __aiter__(self):
                1/0
        async def foo():
            nonlocal CNT
            with self.assertWarnsRegex(PendingDeprecationWarning, "legacy"):
                async for i in AI():
                    CNT += 1
            CNT += 10
        with self.assertRaises(ZeroDivisionError):
            run_async(foo())
        self.assertEqual(CNT, 0)

    def test_for_8(self):
        CNT = 0
        class AI:
            def __aiter__(self):
                1/0
        async def foo():
            nonlocal CNT
            async for i in AI():
                CNT += 1
            CNT += 10
        with self.assertRaises(ZeroDivisionError):
            run_async(foo())
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                # Test that if __aiter__ raises an exception it propagates
                # without any kind of warning.
                run_async(foo())
        self.assertEqual(CNT, 0)

    @min_py27
    def test_for_9(self):
        # Test that PendingDeprecationWarning can safely be converted into
        # an exception (__aiter__ should not have a chance to raise
        # a ZeroDivisionError.)
        class AI:
            async def __aiter__(self):
                1/0
        async def foo():
            async for i in AI():
                pass

        with self.assertRaises(PendingDeprecationWarning):
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                run_async(foo())

    @min_py27
    def test_for_10(self):
        # Test that PendingDeprecationWarning can safely be converted into
        # an exception.
        class AI:
            async def __aiter__(self):
                pass
        async def foo():
            async for i in AI():
                pass

        with self.assertRaises(PendingDeprecationWarning):
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                run_async(foo())

    def test_copy(self):
        async def func(): pass
        coro = func()
        with self.assertRaises(TypeError):
            copy.copy(coro)

        aw = coro.__await__()
        try:
            with self.assertRaises(TypeError):
                copy.copy(aw)
        finally:
            aw.close()

    def test_pickle(self):
        async def func(): pass
        coro = func()
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            with self.assertRaises((TypeError, pickle.PicklingError)):
                pickle.dumps(coro, proto)

        aw = coro.__await__()
        try:
            for proto in range(pickle.HIGHEST_PROTOCOL + 1):
                with self.assertRaises((TypeError, pickle.PicklingError)):
                    pickle.dumps(aw, proto)
        finally:
            aw.close()


class CoroAsyncIOCompatTest(unittest.TestCase):

    def test_asyncio_1(self):
        import asyncio

        class MyException(Exception):
            pass

        buffer = []

        class CM(object):
            async def __aenter__(self):
                buffer.append(1)
                await asyncio.sleep(0.01)
                buffer.append(2)
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                await asyncio.sleep(0.01)
                buffer.append(exc_type.__name__)

        async def f():
            async with CM() as c:
                await asyncio.sleep(0.01)
                raise MyException
            buffer.append('unreachable')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(f())
        except MyException:
            pass
        finally:
            loop.close()
            asyncio.set_event_loop(None)

        self.assertEqual(buffer, [1, 2, 'MyException'])


class SysSetCoroWrapperTest(unittest.TestCase):

    def test_set_wrapper_1(self):
        async def foo():
            return 'spam'

        wrapped = None
        def wrap(gen):
            nonlocal wrapped
            wrapped = gen
            return gen

        self.assertIsNone(sys.get_coroutine_wrapper())

        sys.set_coroutine_wrapper(wrap)
        self.assertIs(sys.get_coroutine_wrapper(), wrap)
        try:
            f = foo()
            self.assertTrue(wrapped)

            self.assertEqual(run_async(f), ([], 'spam'))
        finally:
            sys.set_coroutine_wrapper(None)

        self.assertIsNone(sys.get_coroutine_wrapper())

        wrapped = None
        with silence_coro_gc():
            foo()
        self.assertFalse(wrapped)

    def test_set_wrapper_2(self):
        self.assertIsNone(sys.get_coroutine_wrapper())
        with self.assertRaisesRegex(TypeError, "callable expected, got int"):
            sys.set_coroutine_wrapper(1)
        self.assertIsNone(sys.get_coroutine_wrapper())

    def test_set_wrapper_3(self):
        async def foo():
            return 'spam'

        def wrapper(coro):
            async def wrap(coro):
                return await coro
            return wrap(coro)

        sys.set_coroutine_wrapper(wrapper)
        try:
            with silence_coro_gc(), self.assertRaisesRegex(
                RuntimeError,
                "coroutine wrapper.*\.wrapper at 0x.*attempted to "
                "recursively wrap .* wrap .*"):

                foo()
        finally:
            sys.set_coroutine_wrapper(None)

    def test_set_wrapper_4(self):
        @types_coroutine
        def foo():
            return 'spam'

        wrapped = None
        def wrap(gen):
            nonlocal wrapped
            wrapped = gen
            return gen

        sys.set_coroutine_wrapper(wrap)
        try:
            foo()
            self.assertIs(
                wrapped, None,
                "generator-based coroutine was wrapped via "
                "sys.set_coroutine_wrapper")
        finally:
            sys.set_coroutine_wrapper(None)


class CAPITest(unittest.TestCase):

    def test_tp_await_1(self):
        from _testcapi import awaitType as at

        async def foo():
            future = at(iter([1]))
            return (await future)

        self.assertEqual(foo().send(None), 1)

    def test_tp_await_2(self):
        # Test tp_await to __await__ mapping
        from _testcapi import awaitType as at
        future = at(iter([1]))
        self.assertEqual(next(future.__await__()), 1)

    def test_tp_await_3(self):
        from _testcapi import awaitType as at

        async def foo():
            future = at(1)
            return (await future)

        with self.assertRaisesRegex(
                TypeError, "__await__.*returned non-iterator of type 'int'"):
            self.assertEqual(foo().send(None), 1)


# disable some tests that only apply to CPython

# TODO?
if True or sys.version_info < (3, 5):
    SysSetCoroWrapperTest = None
    CAPITest = None

if sys.version_info < (3, 5):  # (3, 4, 4)
    CoroAsyncIOCompatTest = None
else:
    try:
        import asyncio
    except ImportError:
        CoroAsyncIOCompatTest = None

if __name__=="__main__":
    unittest.main()
