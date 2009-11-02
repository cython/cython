dict_size = 4
d = dict(zip(range(10,dict_size+10), range(dict_size)))

def items(dict d):
    """
    >>> items(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    """
    l = []
    for k,v in d.items():
        l.append((k,v))
    l.sort()
    return l

def iteritems(dict d):
    """
    >>> iteritems(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    """
    l = []
    for k,v in d.iteritems():
        l.append((k,v))
    l.sort()
    return l

def iteritems_int(dict d):
    """
    >>> iteritems_int(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    """
    cdef int k,v
    l = []
    for k,v in d.iteritems():
        l.append((k,v))
    l.sort()
    return l

def iteritems_tuple(dict d):
    """
    >>> iteritems_tuple(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    """
    l = []
    for t in d.iteritems():
        l.append(t)
    l.sort()
    return l

def iteritems_listcomp(dict d):
    cdef list l = [(k,v) for k,v in d.iteritems()]
    l.sort()
    return l

def iterkeys(dict d):
    """
    >>> iterkeys(d)
    [10, 11, 12, 13]
    """
    l = []
    for k in d.iterkeys():
        l.append(k)
    l.sort()
    return l

def iterkeys_int(dict d):
    """
    >>> iterkeys_int(d)
    [10, 11, 12, 13]
    """
    cdef int k
    l = []
    for k in d.iterkeys():
        l.append(k)
    l.sort()
    return l

def iterdict(dict d):
    """
    >>> iterdict(d)
    [10, 11, 12, 13]
    """
    l = []
    for k in d:
        l.append(k)
    l.sort()
    return l

def iterdict_int(dict d):
    """
    >>> iterdict_int(d)
    [10, 11, 12, 13]
    """
    cdef int k
    l = []
    for k in d:
        l.append(k)
    l.sort()
    return l

def iterdict_reassign(dict d):
    """
    >>> iterdict_reassign(d)
    [10, 11, 12, 13]
    """
    cdef dict d_new = {}
    l = []
    for k in d:
        d = d_new
        l.append(k)
    l.sort()
    return l

def iterdict_listcomp(dict d):
    cdef list l = [k for k in d]
    l.sort()
    return l

def itervalues(dict d):
    """
    >>> itervalues(d)
    [0, 1, 2, 3]
    """
    l = []
    for v in d.itervalues():
        l.append(v)
    l.sort()
    return l

def itervalues_int(dict d):
    """
    >>> itervalues_int(d)
    [0, 1, 2, 3]
    """
    cdef int v
    l = []
    for v in d.itervalues():
        l.append(v)
    l.sort()
    return l

def itervalues_listcomp(dict d):
    cdef list l = [v for v in d.itervalues()]
    l.sort()
    return l
