# mode: run
# tag: asyncgen

class Suspend:
    def __await__(self):
        yield


async def agen():
    try:
        yield 1
    finally:
        for _ in range(3):
            try:
                await Suspend()
            except ValueError:
                pass


def test_throw_into_pending_aclose():
    """
    Throwing into a pending aclose() awaitable while the generator suspends
    again in its cleanup must not crash (no exception is set at that point).

    >>> test_throw_into_pending_aclose()
    first value 1
    aclose send -> None
    aclose throw -> None
    aclose send -> None
    closed
    """
    g = agen()
    try:
        g.__anext__().send(None)
    except StopIteration as stop:
        print("first value %s" % stop.value)
    closer = g.aclose()
    print("aclose send -> %s" % closer.send(None))
    print("aclose throw -> %s" % closer.throw(ValueError()))
    print("aclose send -> %s" % closer.send(None))
    try:
        closer.send(None)
    except StopIteration:
        print("closed")
