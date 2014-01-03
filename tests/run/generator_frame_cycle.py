# mode: run
# tag: generator

import sys

def _next(it):
    if sys.version_info[0] >= 3:
        return next(it)
    else:
        return it.next()

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
    _next(g)
    # Frame object cycle
    eval('g.throw(ValueError)', {'g': g})
    del g
    return tuple(testit)
