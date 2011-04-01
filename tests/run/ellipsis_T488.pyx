# ticket: 488

"""
>>> test()
"""
def test():
    x = ...
    assert x is Ellipsis

    d = {}
    d[...] = 1
    assert d[...] == 1
    del d[...]
    assert ... not in d

    d[..., ...] = 1
    assert d[..., ...] == 1
    assert d[..., Ellipsis] == 1
    assert (Ellipsis, Ellipsis) in d
    del d[..., ...]
    assert (Ellipsis, Ellipsis) not in d

