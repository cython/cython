__doc__ = u"""
>>> ret = repeat_iter()
>>> for s in ret:
...     print(s)
a
a
b
b
c
c
"""

def repeat_iter():
    cdef dict e
    cdef unicode s
    ret = []
    e = {u"A": u"a", u"B": u"b", u"C": u"c"}
    for s in e.itervalues():
        ret.append(s)
    for s in e.itervalues():
        ret.append(s)

    ret.sort()
    return ret
