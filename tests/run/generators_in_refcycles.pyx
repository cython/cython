
import sys
def _next(it):
    if sys.version_info[0] >= 3:
        return next(it)
    else:
        return it.next()

def test_reference_cycle_cleanup():
    """
    >>> import gc
    >>> delegator, gen, deleted = test_reference_cycle_cleanup()

    >>> _next(delegator(gen()))
    123
    >>> _ = gc.collect(); print(sorted(deleted))
    ['bar', 'foo']
    """
    deleted = []
    class Destructed(object):
        def __init__(self, name):
            self.name = name

        def __del__(self):
            deleted.append(self.name)

    def delegator(c):
        d = Destructed('foo')
        yield from c

    def gen():
        d = Destructed('bar')
        while True:
            yield 123

    return delegator, gen, deleted
