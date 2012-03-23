
def test_reference_cycle_cleanup():
    """
    >>> import gc
    >>> delegator, gen, next, deleted = test_reference_cycle_cleanup()

    >>> next(delegator(gen()))
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

    return delegator, gen, next, deleted
