# mode: run
# tag: generator

import cython
import sys


def test_generator_frame_cycle():
    """
    >>> test_generator_frame_cycle()
    ("I'm done",)
    """
    testit = []
    def whoo():
        try:
            yield
        except:
            yield
        finally:
            testit.append("I'm done")
    g = whoo()
    next(g)

    # Frame object cycle
    eval('g.throw(ValueError)', {'g': g})
    del g

    return tuple(testit)


def test_generator_frame_cycle_with_outer_exc():
    """
    >>> test_generator_frame_cycle_with_outer_exc()
    ("I'm done",)
    """
    testit = []
    def whoo():
        try:
            yield
        except:
            yield
        finally:
            testit.append("I'm done")
    g = whoo()
    next(g)

    try:
        raise ValueError()
    except ValueError as exc:
        assert sys.exc_info()[1] is exc, sys.exc_info()
        # Frame object cycle
        eval('g.throw(ValueError)', {'g': g})
        # CPython 3.3 handles this incorrectly itself :)
        assert sys.exc_info()[1] is exc, sys.exc_info()
        del g
        assert sys.exc_info()[1] is exc, sys.exc_info()

    return tuple(testit)
