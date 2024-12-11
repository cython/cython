# mode: run

from __future__ import print_function

import threading
import sys

def make_thread_func(barrier, failed, done, body):
    def thread_func():
        barrier.wait()
        while not done.is_set() and not failed.is_set():
            # Acceptable things to happen:
            # 1. We successfully get the next value.
            # 2. The iteration has finished completely.
            # 3. The generator is already executing in another thread
            # Unacceptable things to happen:
            # 1. The generator runs in multiple threads, giving a miscount
            # 2. Any other exception
            try:
                body()
            except StopIteration:
                pass  # OK
            except ValueError as e:
                if "already executing" not in e.args[0]:
                    failed.set()
                    raise  # otherwise OK
            except BaseException as e:
                failed.set()
                raise
    return thread_func

def test_simple_generator(n_threads, n_loops):
    """
    >>> test_simple_generator(4, 500)
    >>> test_simple_generator(4, 500)
    >>> test_simple_generator(4, 500)
    >>> test_simple_generator(4, 500)
    >>> test_simple_generator(4, 500)
    >>> test_simple_generator(4, 500)
    """
    barrier = threading.Barrier(n_threads)
    done = threading.Event()
    failed = threading.Event()
    count = 0

    def gen():
        nonlocal count
        try:
            for i in range(n_loops):
                count += 1
                yield
        finally:
            done.set()

    g = gen()

    threads = [ 
        threading.Thread(
            target=make_thread_func(
                barrier=barrier,
                failed=failed,
                done=done,
                body=lambda: next(g)
            )
        ) for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not failed.is_set()
    assert count == n_loops, (count, n_loops)

def test_yield_from_generator(n_threads, n_loops):
    """
    >>> test_yield_from_generator(4, 500)
    >>> test_yield_from_generator(4, 500)
    >>> test_yield_from_generator(4, 500)
    >>> test_yield_from_generator(4, 500)
    >>> test_yield_from_generator(4, 500)
    >>> test_yield_from_generator(4, 500)
    """
    barrier = threading.Barrier(n_threads)
    done = threading.Event()
    failed = threading.Event()
    count = 0

    def gen():
        nonlocal count
        try:
            for i in range(n_loops):
                count += 1
                yield
        finally:
            done.set()

    def gen2(other):
        yield from other

    g = gen2(gen())

    threads = [ 
        threading.Thread(
            target=make_thread_func(
                barrier=barrier,
                failed=failed,
                done=done,
                body=lambda: next(g)
            )
        ) for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not failed.is_set()
    assert count == n_loops, (count, n_loops)

def test_value_into_generator(n_threads, n_loops):
    """
    >>> test_value_into_generator(4, 500)
    >>> test_value_into_generator(4, 500)
    >>> test_value_into_generator(4, 500)
    >>> test_value_into_generator(4, 500)
    >>> test_value_into_generator(4, 500)
    >>> test_value_into_generator(4, 500)
    """
    barrier = threading.Barrier(n_threads)
    done = threading.Event()
    failed = threading.Event()
    count = 0

    def gen():
        nonlocal count
        try:
            for i in range(n_loops):
                count += 1
                value = yield count
                assert value == "hello"
        finally:
            done.set()

    g = gen()
    next(g)

    def body():
        out = g.send("hello")
        assert isinstance(out, int), out

    threads = [ 
        threading.Thread(
            target=make_thread_func(
                barrier=barrier,
                failed=failed,
                done=done,
                body=body
            )
        ) for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not failed.is_set()
    assert count == n_loops, (count, n_loops)

class MyError(Exception):
    pass

def test_throw_into_generator(n_threads, n_loops):
    """
    >>> test_throw_into_generator(4, 500)
    >>> test_throw_into_generator(4, 500)
    >>> test_throw_into_generator(4, 500)
    >>> test_throw_into_generator(4, 500)
    >>> test_throw_into_generator(4, 500)
    >>> test_throw_into_generator(4, 500)
    >>> test_throw_into_generator(4, 500)
    >>> test_throw_into_generator(4, 500)
    """
    barrier = threading.Barrier(n_threads)
    done = threading.Event()
    failed = threading.Event()
    count = 0

    def gen():
        nonlocal count
        try:
            for i in range(n_loops):
                count += 1
                try:
                    yield
                except MyError:
                    pass  # good
                else:
                    assert False, "We're supposed to get an exception!"
        finally:
            done.set()

    g = gen()
    next(g)

    def body():
        try:
            g.throw(MyError())
        except MyError:
            if not done.is_set():
                raise
            # For an exhausted generator the correct behaviour is to rethrow
            # the error that was passed to it, so swallow the exception in this case. 
            pass

    threads = [ 
        threading.Thread(
            target=make_thread_func(
                barrier=barrier,
                failed=failed,
                done=done,
                body=body
            )
        ) for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not failed.is_set()
    assert count == n_loops, (count, n_loops)