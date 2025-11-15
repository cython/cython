# cython: language_level=3, binding=True
# mode: run
# tag: pep525, asyncfor, await

from __future__ import generator_stop

import cython

import os
import sys
#import inspect
#import types
import unittest
import contextlib

#from unittest import mock

#from test.support import import_module

#asyncio = import_module("asyncio")

ZERO = 0

try:
    import asyncio
except ImportError:
    try:
        from unittest import skip
    except ImportError:
        def requires_asyncio(c):
            return None
    else:
        requires_asyncio = skip("tests require asyncio")
    asyncio = None
else:
    def requires_asyncio(c):
        return c


def not_pypy(f):
    if getattr(sys, "pypy_version_info", False):
        from unittest import skip
        return skip("cannot run on PyPy due to finalizer")(f)
    return f

def not_limited_api(f):
    # CYTHON_COMPILING_IN_LIMITED_API exposed in PXD
    if cython.compiled and CYTHON_COMPILING_IN_LIMITED_API:
        from unittest import skip
        return skip("Cannot run in Limited API due to finalizer")(f)
    return f

try:
    from types import coroutine as types_coroutine
except ImportError:
    def types_coroutine(func):
        from functools import wraps
        wrapped = wraps(func)

        # copied from types.py in Py3.6
        class _GeneratorWrapper(object):
            # TODO: Implement this in C.
            def __init__(self, gen):
                self.__wrapped = gen
                self.__isgen = hasattr(gen, 'gi_running')
                self.__name__ = getattr(gen, '__name__', None)
                self.__qualname__ = getattr(gen, '__qualname__', None)

            def send(self, val):
                return self.__wrapped.send(val)

            def throw(self, tp, *rest):
                return self.__wrapped.throw(tp, *rest)

            def close(self):
                return self.__wrapped.close()

            @property
            def gi_code(self):
                return self.__wrapped.gi_code

            @property
            def gi_frame(self):
                return self.__wrapped.gi_frame

            @property
            def gi_running(self):
                return self.__wrapped.gi_running

            @property
            def gi_yieldfrom(self):
                return self.__wrapped.gi_yieldfrom

            cr_code = gi_code
            cr_frame = gi_frame
            cr_running = gi_running
            cr_await = gi_yieldfrom

            def __next__(self):
                return next(self.__wrapped)
            next = __next__

            def __iter__(self):
                if self.__isgen:
                    return self.__wrapped
                return self

            __await__ = __iter__

        @wrapped
        def call(*args, **kwargs):
            return wrapped(_GeneratorWrapper(func(*args, **kwargs)))

        return call

try:
    from inspect import isawaitable as inspect_isawaitable
except ImportError:
    def inspect_isawaitable(o):
        return hasattr(o, '__await__')


# compiled exec()
def exec(code_string, l, g):
    from Cython.Compiler.Errors import CompileError
    from Cython.Shadow import inline
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    old_stderr = sys.stderr
    try:
        sys.stderr = StringIO()
        ns = inline(code_string, locals=l, globals=g, lib_dir=os.path.dirname(__file__))
    except CompileError as exc:
        raise SyntaxError(str(exc))
    finally:
        sys.stderr = old_stderr
    g.update(ns)


class AwaitException(Exception):
    pass


@types_coroutine
def awaitable(*, throw=False):
    if throw:
        yield ('throw',)
    else:
        yield ('result',)


def run_until_complete(coro):
    exc = False
    while True:
        try:
            if exc:
                exc = False
                fut = coro.throw(AwaitException)
            else:
                fut = coro.send(None)
        except StopIteration as ex:
            return ex.args[0]

        if fut == ('throw',):
            exc = True


def to_list(gen):
    async def iterate():
        res = []
        async for i in gen:
            res.append(i)
        return res

    return run_until_complete(iterate())


class AsyncGenSyntaxTest(unittest.TestCase):

    @contextlib.contextmanager
    def assertRaisesRegex(self, exc_type, regex):
        # the error messages usually don't match, so we just ignore them
        try:
            yield
        except exc_type:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_async_gen_syntax_01(self):
        code = '''async def foo():
            await abc
            yield from 123
        '''

        with self.assertRaisesRegex(SyntaxError, 'yield from.*inside async'):
            exec(code, {}, {})

    def test_async_gen_syntax_02(self):
        code = '''async def foo():
            yield from 123
        '''

        with self.assertRaisesRegex(SyntaxError, 'yield from.*inside async'):
            exec(code, {}, {})

    def test_async_gen_syntax_03(self):
        code = '''async def foo():
            await abc
            yield
            return 123
        '''

        with self.assertRaisesRegex(SyntaxError, 'return.*value.*async gen'):
            exec(code, {}, {})

    def test_async_gen_syntax_04(self):
        code = '''async def foo():
            yield
            return 123
        '''

        with self.assertRaisesRegex(SyntaxError, 'return.*value.*async gen'):
            exec(code, {}, {})

    def test_async_gen_syntax_05(self):
        code = '''async def foo():
            if 0:
                yield
            return 12
        '''

        with self.assertRaisesRegex(SyntaxError, 'return.*value.*async gen'):
            exec(code, {}, {})


class AsyncGenTest(unittest.TestCase):

    def compare_generators(self, sync_gen, async_gen):
        def sync_iterate(g):
            res = []
            while True:
                try:
                    res.append(next(g))
                except StopIteration:
                    res.append('STOP')
                    break
                except Exception as ex:
                    res.append(str(type(ex)))
            return res

        def async_iterate(g):
            res = []
            while True:
                an = g.__anext__()
                try:
                    while True:
                        try:
                            next(an)
                        except StopIteration as ex:
                            if ex.args:
                                res.append(ex.args[0])
                                break
                            else:
                                res.append('EMPTY StopIteration')
                                break
                        except StopAsyncIteration:
                            raise
                        except Exception as ex:
                            res.append(str(type(ex)))
                            break
                except StopAsyncIteration:
                    res.append('STOP')
                    break
            return res

        sync_gen_result = sync_iterate(sync_gen)
        async_gen_result = async_iterate(async_gen)
        self.assertEqual(sync_gen_result, async_gen_result)
        return async_gen_result

    def test_async_gen_iteration_01(self):
        async def gen():
            await awaitable()
            a = yield 123
            self.assertIs(a, None)
            await awaitable()
            yield 456
            await awaitable()
            yield 789

        self.assertEqual(to_list(gen()), [123, 456, 789])

    def test_async_gen_iteration_02(self):
        async def gen():
            await awaitable()
            yield 123
            await awaitable()

        g = gen()
        ai = g.__aiter__()

        an = ai.__anext__()
        self.assertEqual(next(an), ('result',))

        try:
            next(an)
        except StopIteration as ex:
            self.assertEqual(ex.args[0], 123)
        else:
            self.fail('StopIteration was not raised')

        an = ai.__anext__()
        self.assertEqual(next(an), ('result',))

        try:
            next(an)
        except StopAsyncIteration as ex:
            self.assertFalse(ex.args)
        else:
            self.fail('StopAsyncIteration was not raised')

    def test_async_gen_exception_03(self):
        async def gen():
            await awaitable()
            yield 123
            await awaitable(throw=True)
            yield 456

        with self.assertRaises(AwaitException):
            to_list(gen())

    def test_async_gen_exception_04(self):
        async def gen():
            await awaitable()
            yield 123
            1 / ZERO

        g = gen()
        ai = g.__aiter__()

        an = ai.__anext__()
        self.assertEqual(next(an), ('result',))

        try:
            next(an)
        except StopIteration as ex:
            self.assertEqual(ex.args[0], 123)
        else:
            self.fail('StopIteration was not raised')

        with self.assertRaises(ZeroDivisionError):
            next(ai.__anext__())

    def test_async_gen_exception_05(self):
        async def gen():
            yield 123
            raise StopAsyncIteration

        with self.assertRaisesRegex(RuntimeError,
                                    'async generator.*StopAsyncIteration'):
            to_list(gen())

    def test_async_gen_exception_06(self):
        async def gen():
            yield 123
            raise StopIteration

        with self.assertRaisesRegex(RuntimeError,
                                    'async generator.*StopIteration'):
            to_list(gen())

    def test_async_gen_exception_07(self):
        def sync_gen():
            try:
                yield 1
                1 / ZERO
            finally:
                yield 2
                yield 3

            yield 100

        async def async_gen():
            try:
                yield 1
                1 / ZERO
            finally:
                yield 2
                yield 3

            yield 100

        self.compare_generators(sync_gen(), async_gen())

    def test_async_gen_exception_08(self):
        def sync_gen():
            try:
                yield 1
            finally:
                yield 2
                1 / ZERO
                yield 3

            yield 100

        async def async_gen():
            try:
                yield 1
                await awaitable()
            finally:
                await awaitable()
                yield 2
                1 / ZERO
                yield 3

            yield 100

        self.compare_generators(sync_gen(), async_gen())

    def test_async_gen_exception_09(self):
        def sync_gen():
            try:
                yield 1
                1 / ZERO
            finally:
                yield 2
                yield 3

            yield 100

        async def async_gen():
            try:
                await awaitable()
                yield 1
                1 / ZERO
            finally:
                yield 2
                await awaitable()
                yield 3

            yield 100

        self.compare_generators(sync_gen(), async_gen())

    def test_async_gen_exception_10(self):
        async def gen():
            yield 123
        with self.assertRaisesRegex(TypeError,
                                    "non-None value .* async generator"):
            gen().__anext__().send(100)

    def test_async_gen_exception_11(self):
        def sync_gen():
            yield 10
            yield 20

        def sync_gen_wrapper():
            yield 1
            sg = sync_gen()
            sg.send(None)
            try:
                sg.throw(GeneratorExit())
            except GeneratorExit:
                yield 2
            yield 3

        async def async_gen():
            yield 10
            yield 20

        async def async_gen_wrapper():
            yield 1
            asg = async_gen()
            await asg.asend(None)
            try:
                await asg.athrow(GeneratorExit())
            except GeneratorExit:
                yield 2
            yield 3

        self.compare_generators(sync_gen_wrapper(), async_gen_wrapper())

    def test_async_gen_api_01(self):
        async def gen():
            yield 123

        g = gen()

        self.assertEqual(g.__name__, 'gen')
        g.__name__ = '123'
        self.assertEqual(g.__name__, '123')

        self.assertIn('.gen', g.__qualname__)
        g.__qualname__ = '123'
        self.assertEqual(g.__qualname__, '123')

        #self.assertIsNone(g.ag_await)
        #self.assertIsInstance(g.ag_frame, types.FrameType)
        self.assertFalse(g.ag_running)
        #self.assertIsInstance(g.ag_code, types.CodeType)

        self.assertTrue(inspect_isawaitable(g.aclose()))


@requires_asyncio
class AsyncGenAsyncioTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()
        self.loop = None

    async def to_list(self, gen):
        res = []
        async for i in gen:
            res.append(i)
        return res

    def test_async_gen_asyncio_01(self):
        async def gen():
            yield 1
            await asyncio.sleep(0.01)
            yield 2
            await asyncio.sleep(0.01)
            return
            yield 3

        res = self.loop.run_until_complete(self.to_list(gen()))
        self.assertEqual(res, [1, 2])

    def test_async_gen_asyncio_02(self):
        async def gen():
            yield 1
            await asyncio.sleep(0.01)
            yield 2
            1 / ZERO
            yield 3

        with self.assertRaises(ZeroDivisionError):
            self.loop.run_until_complete(self.to_list(gen()))

    def test_async_gen_asyncio_03(self):
        loop = self.loop

        class Gen:
            async def __aiter__(self):
                yield 1
                await asyncio.sleep(0.01)
                yield 2

        res = loop.run_until_complete(self.to_list(Gen()))
        self.assertEqual(res, [1, 2])

    def test_async_gen_asyncio_anext_04(self):
        async def foo():
            yield 1
            await asyncio.sleep(0.01)
            try:
                yield 2
                yield 3
            except ZeroDivisionError:
                yield 1000
            await asyncio.sleep(0.01)
            yield 4

        async def run1():
            it = foo().__aiter__()

            self.assertEqual(await it.__anext__(), 1)
            self.assertEqual(await it.__anext__(), 2)
            self.assertEqual(await it.__anext__(), 3)
            self.assertEqual(await it.__anext__(), 4)
            with self.assertRaises(StopAsyncIteration):
                await it.__anext__()
            with self.assertRaises(StopAsyncIteration):
                await it.__anext__()

        async def run2():
            it = foo().__aiter__()

            self.assertEqual(await it.__anext__(), 1)
            self.assertEqual(await it.__anext__(), 2)
            try:
                it.__anext__().throw(ZeroDivisionError)
            except StopIteration as ex:
                self.assertEqual(ex.args[0], 1000)
            else:
                self.fail('StopIteration was not raised')
            self.assertEqual(await it.__anext__(), 4)
            with self.assertRaises(StopAsyncIteration):
                await it.__anext__()

        self.loop.run_until_complete(run1())
        self.loop.run_until_complete(run2())

    def test_async_gen_asyncio_anext_05(self):
        async def foo():
            v = yield 1
            v = yield v
            yield v * 100

        async def run():
            it = foo().__aiter__()

            try:
                it.__anext__().send(None)
            except StopIteration as ex:
                self.assertEqual(ex.args[0], 1)
            else:
                self.fail('StopIteration was not raised')

            try:
                it.__anext__().send(10)
            except StopIteration as ex:
                self.assertEqual(ex.args[0], 10)
            else:
                self.fail('StopIteration was not raised')

            try:
                it.__anext__().send(12)
            except StopIteration as ex:
                self.assertEqual(ex.args[0], 1200)
            else:
                self.fail('StopIteration was not raised')

            with self.assertRaises(StopAsyncIteration):
                await it.__anext__()

        self.loop.run_until_complete(run())

    def test_async_gen_asyncio_anext_06(self):
        DONE = 0

        # test synchronous generators
        def foo():
            try:
                yield
            except:
                pass
        g = foo()
        g.send(None)
        with self.assertRaises(StopIteration):
            g.send(None)

        # now with asynchronous generators

        async def gen():
            nonlocal DONE
            try:
                yield
            except:
                pass
            DONE = 1

        async def run():
            nonlocal DONE
            g = gen()
            await g.asend(None)
            with self.assertRaises(StopAsyncIteration):
                await g.asend(None)
            DONE += 10

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 11)

    def test_async_gen_asyncio_anext_tuple(self):
        async def foo():
            try:
                yield (1,)
            except ZeroDivisionError:
                yield (2,)

        async def run():
            it = foo().__aiter__()

            self.assertEqual(await it.__anext__(), (1,))
            with self.assertRaises(StopIteration) as cm:
                it.__anext__().throw(ZeroDivisionError)
            self.assertEqual(cm.exception.args[0], (2,))
            with self.assertRaises(StopAsyncIteration):
                await it.__anext__()

        self.loop.run_until_complete(run())

    def test_async_gen_asyncio_anext_stopiteration(self):
        async def foo():
            try:
                yield StopIteration(1)
            except ZeroDivisionError:
                yield StopIteration(3)

        async def run():
            it = foo().__aiter__()

            v = await it.__anext__()
            self.assertIsInstance(v, StopIteration)
            self.assertEqual(v.value, 1)
            with self.assertRaises(StopIteration) as cm:
                it.__anext__().throw(ZeroDivisionError)
            v = cm.exception.args[0]
            self.assertIsInstance(v, StopIteration)
            self.assertEqual(v.value, 3)
            with self.assertRaises(StopAsyncIteration):
                await it.__anext__()

        self.loop.run_until_complete(run())

    def test_async_gen_asyncio_aclose_06(self):
        async def foo():
            try:
                yield 1
                1 / ZERO
            finally:
                await asyncio.sleep(0.01)
                yield 12

        async def run():
            gen = foo()
            it = gen.__aiter__()
            await it.__anext__()
            await gen.aclose()

        with self.assertRaisesRegex(
                RuntimeError,
                "async generator ignored GeneratorExit"):
            self.loop.run_until_complete(run())

    def test_async_gen_asyncio_aclose_07(self):
        DONE = 0

        async def foo():
            nonlocal DONE
            try:
                yield 1
                1 / ZERO
            finally:
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE += 1
            DONE += 1000

        async def run():
            gen = foo()
            it = gen.__aiter__()
            await it.__anext__()
            await gen.aclose()

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_aclose_08(self):
        DONE = 0

        fut = asyncio.Future(loop=self.loop)

        async def foo():
            nonlocal DONE
            try:
                yield 1
                await fut
                DONE += 1000
                yield 2
            finally:
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE += 1
            DONE += 1000

        async def run():
            gen = foo()
            it = gen.__aiter__()
            self.assertEqual(await it.__anext__(), 1)
            await gen.aclose()

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

        # Silence ResourceWarnings
        fut.cancel()
        self.loop.run_until_complete(asyncio.sleep(0.01))

    @not_pypy
    @not_limited_api
    def test_async_gen_asyncio_gc_aclose_09(self):
        DONE = 0

        async def gen():
            nonlocal DONE
            try:
                while True:
                    yield 1
            finally:
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE = 1

        async def run():
            g = gen()
            await g.__anext__()
            await g.__anext__()
            del g

            await asyncio.sleep(0.2)

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_aclose_10(self):
        DONE = 0

        # test synchronous generators
        def foo():
            try:
                yield
            except:
                pass
        g = foo()
        g.send(None)
        g.close()

        # now with asynchronous generators

        async def gen():
            nonlocal DONE
            try:
                yield
            except:
                pass
            DONE = 1

        async def run():
            nonlocal DONE
            g = gen()
            await g.asend(None)
            await g.aclose()
            DONE += 10

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 11)

    def test_async_gen_asyncio_aclose_11(self):
        DONE = 0

        # test synchronous generators
        def foo():
            try:
                yield
            except:
                pass
            yield
        g = foo()
        g.send(None)
        with self.assertRaisesRegex(RuntimeError, 'ignored GeneratorExit'):
            g.close()

        # now with asynchronous generators

        async def gen():
            nonlocal DONE
            try:
                yield
            except:
                pass
            yield
            DONE += 1

        async def run():
            nonlocal DONE
            g = gen()
            await g.asend(None)
            with self.assertRaisesRegex(RuntimeError, 'ignored GeneratorExit'):
                await g.aclose()
            DONE += 10

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 10)

    def test_async_gen_asyncio_aclose_12(self):
        DONE = 0

        async def target():
            await asyncio.sleep(0.01)
            1 / ZERO

        async def foo():
            nonlocal DONE
            task = self.loop.create_task(target())
            try:
                yield 1
            finally:
                try:
                    await task
                except ZeroDivisionError:
                    DONE = 1

        async def run():
            gen = foo()
            it = gen.__aiter__()
            await it.__anext__()
            await gen.aclose()

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_asend_01(self):
        DONE = 0

        # Sanity check:
        def sgen():
            v = yield 1
            yield v * 2
        sg = sgen()
        v = sg.send(None)
        self.assertEqual(v, 1)
        v = sg.send(100)
        self.assertEqual(v, 200)

        async def gen():
            nonlocal DONE
            try:
                await asyncio.sleep(0.01)
                v = yield 1
                await asyncio.sleep(0.01)
                yield v * 2
                await asyncio.sleep(0.01)
                return
            finally:
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE = 1

        async def run():
            g = gen()

            v = await g.asend(None)
            self.assertEqual(v, 1)

            v = await g.asend(100)
            self.assertEqual(v, 200)

            with self.assertRaises(StopAsyncIteration):
                await g.asend(None)

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_asend_02(self):
        DONE = 0

        async def sleep_n_crash(delay):
            await asyncio.sleep(delay)
            1 / ZERO

        async def gen():
            nonlocal DONE
            try:
                await asyncio.sleep(0.01)
                v = yield 1
                await sleep_n_crash(0.01)
                DONE += 1000
                yield v * 2
            finally:
                assert sys.exc_info()[0] == ZeroDivisionError
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE += 1

        async def run():
            g = gen()

            v = await g.asend(None)
            self.assertEqual(v, 1)

            await g.asend(100)

        with self.assertRaises(ZeroDivisionError):
            self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_asend_03(self):
        DONE = 0

        async def sleep_n_crash(delay):
            fut = asyncio.ensure_future(asyncio.sleep(delay),
                                        loop=self.loop)
            self.loop.call_later(delay / 2, lambda: fut.cancel())
            return await fut

        async def gen():
            nonlocal DONE
            try:
                await asyncio.sleep(0.01)
                v = yield 1
                await sleep_n_crash(0.01)
                DONE += 1000
                yield v * 2
            finally:
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE = 1

        async def run():
            g = gen()

            v = await g.asend(None)
            self.assertEqual(v, 1)

            await g.asend(100)

        with self.assertRaises(asyncio.CancelledError):
            self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_athrow_01(self):
        DONE = 0

        class FooEr(Exception):
            pass

        # Sanity check:
        def sgen():
            try:
                v = yield 1
            except FooEr:
                v = 1000
            yield v * 2
        sg = sgen()
        v = sg.send(None)
        self.assertEqual(v, 1)
        v = sg.throw(FooEr)
        self.assertEqual(v, 2000)
        with self.assertRaises(StopIteration):
            sg.send(None)

        async def gen():
            nonlocal DONE
            try:
                await asyncio.sleep(0.01)
                try:
                    v = yield 1
                except FooEr:
                    v = 1000
                    await asyncio.sleep(0.01)
                yield v * 2
                await asyncio.sleep(0.01)
                # return
            finally:
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE = 1

        async def run():
            g = gen()

            v = await g.asend(None)
            self.assertEqual(v, 1)

            v = await g.athrow(FooEr)
            self.assertEqual(v, 2000)

            with self.assertRaises(StopAsyncIteration):
                await g.asend(None)

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_athrow_02(self):
        DONE = 0

        class FooEr(Exception):
            pass

        async def sleep_n_crash(delay):
            fut = asyncio.ensure_future(asyncio.sleep(delay),
                                        loop=self.loop)
            self.loop.call_later(delay / 2, lambda: fut.cancel())
            return await fut

        async def gen():
            nonlocal DONE
            try:
                await asyncio.sleep(0.01)
                try:
                    v = yield 1
                except FooEr:
                    await sleep_n_crash(0.01)
                yield v * 2
                await asyncio.sleep(0.01)
                # return
            finally:
                await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)
                DONE = 1

        async def run():
            g = gen()

            v = await g.asend(None)
            self.assertEqual(v, 1)

            try:
                await g.athrow(FooEr)
            except asyncio.CancelledError:
                self.assertEqual(DONE, 1)
                raise
            else:
                self.fail('CancelledError was not raised')

        with self.assertRaises(asyncio.CancelledError):
            self.loop.run_until_complete(run())
        self.assertEqual(DONE, 1)

    def test_async_gen_asyncio_athrow_03(self):
        DONE = 0

        # test synchronous generators
        def foo():
            try:
                yield
            except:
                pass
        g = foo()
        g.send(None)
        with self.assertRaises(StopIteration):
            g.throw(ValueError)

        # now with asynchronous generators

        async def gen():
            nonlocal DONE
            try:
                yield
            except:
                pass
            DONE = 1

        async def run():
            nonlocal DONE
            g = gen()
            await g.asend(None)
            with self.assertRaises(StopAsyncIteration):
                await g.athrow(ValueError)
            DONE += 10

        self.loop.run_until_complete(run())
        self.assertEqual(DONE, 11)

    def test_async_gen_asyncio_athrow_tuple(self):
        async def gen():
            try:
                yield 1
            except ZeroDivisionError:
                yield (2,)

        async def run():
            g = gen()
            v = await g.asend(None)
            self.assertEqual(v, 1)
            v = await g.athrow(ZeroDivisionError)
            self.assertEqual(v, (2,))
            with self.assertRaises(StopAsyncIteration):
                await g.asend(None)

        self.loop.run_until_complete(run())

    def test_async_gen_asyncio_athrow_stopiteration(self):
        async def gen():
            try:
                yield 1
            except ZeroDivisionError:
                yield StopIteration(2)

        async def run():
            g = gen()
            v = await g.asend(None)
            self.assertEqual(v, 1)
            v = await g.athrow(ZeroDivisionError)
            self.assertIsInstance(v, StopIteration)
            self.assertEqual(v.value, 2)
            with self.assertRaises(StopAsyncIteration):
                await g.asend(None)

        self.loop.run_until_complete(run())

    def test_async_gen_asyncio_shutdown_01(self):
        finalized = 0

        async def waiter(timeout):
            nonlocal finalized
            try:
                await asyncio.sleep(timeout)
                yield 1
            finally:
                await asyncio.sleep(0)
                finalized += 1

        async def wait():
            async for _ in waiter(1):
                pass

        t1 = self.loop.create_task(wait())
        t2 = self.loop.create_task(wait())

        self.loop.run_until_complete(asyncio.sleep(0.1))


        # Silence warnings
        t1.cancel()
        t2.cancel()

        with self.assertRaises(asyncio.CancelledError):
            self.loop.run_until_complete(t1)
        with self.assertRaises(asyncio.CancelledError):
            self.loop.run_until_complete(t2)

        self.loop.run_until_complete(self.loop.shutdown_asyncgens())

        self.assertEqual(finalized, 2)

    """
    def test_async_gen_expression_01(self):
        async def arange(n):
            for i in range(n):
                await asyncio.sleep(0.01)
                yield i

        def make_arange(n):
            # This syntax is legal starting with Python 3.7
            return (i * 2 async for i in arange(n))

        async def run():
            return [i async for i in make_arange(10)]

        res = self.loop.run_until_complete(run())
        self.assertEqual(res, [i * 2 for i in range(10)])

    def test_async_gen_expression_02(self):
        async def wrap(n):
            await asyncio.sleep(0.01)
            return n

        def make_arange(n):
            # This syntax is legal starting with Python 3.7
            return (i * 2 for i in range(n) if await wrap(i))

        async def run():
            return [i async for i in make_arange(10)]

        res = self.loop.run_until_complete(run())
        self.assertEqual(res, [i * 2 for i in range(1, 10)])
    """

    def test_asyncgen_nonstarted_hooks_are_cancellable(self):
        # See https://bugs.python.org/issue38013
        messages = []

        def exception_handler(loop, context):
            messages.append(context)

        async def async_iterate():
            yield 1
            yield 2

        async def main():
            # loop = asyncio.get_running_loop()
            loop = self.loop
            loop.set_exception_handler(exception_handler)

            async for i in async_iterate():
                break

        # asyncio.run(main())
        self.loop.run_until_complete(main())

        self.assertEqual([], messages)

    def test_async_gen_await_same_anext_coro_twice(self):
        async def async_iterate():
            yield 1
            yield 2

        async def run():
            it = async_iterate()
            nxt = it.__anext__()
            await nxt
            with self.assertRaisesRegex(
                    RuntimeError,
                    r"cannot reuse already awaited __anext__\(\)/asend\(\)"
            ):
                await nxt

            await it.aclose()  # prevent unfinished iterator warning

        self.loop.run_until_complete(run())

    def test_async_gen_await_same_aclose_coro_twice(self):
        async def async_iterate():
            yield 1
            yield 2

        async def run():
            it = async_iterate()
            nxt = it.aclose()
            await nxt
            with self.assertRaisesRegex(
                    RuntimeError,
                    r"cannot reuse already awaited aclose\(\)/athrow\(\)"
            ):
                await nxt

        self.loop.run_until_complete(run())

    def test_async_gen_aclose_twice_with_different_coros(self):
        # Regression test for https://bugs.python.org/issue39606
        async def async_iterate():
            yield 1
            yield 2

        async def run():
            it = async_iterate()
            await it.aclose()
            await it.aclose()

        self.loop.run_until_complete(run())

    def test_async_gen_aclose_after_exhaustion(self):
        # Regression test for https://bugs.python.org/issue39606
        async def async_iterate():
            yield 1
            yield 2

        async def run():
            it = async_iterate()
            async for _ in it:
                pass
            await it.aclose()

        self.loop.run_until_complete(run())

    """
    def test_async_gen_aclose_compatible_with_get_stack(self):
        async def async_generator():
            yield object()

        async def run():
            ag = async_generator()
            self.loop.create_task(ag.aclose())
            tasks = asyncio.all_tasks()
            for task in tasks:
                # No AttributeError raised
                task.get_stack()

        self.loop.run_until_complete(run())
    """


if __name__ == "__main__":
    unittest.main()
