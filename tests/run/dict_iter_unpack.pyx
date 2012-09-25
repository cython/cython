# mode: run
# tag: dictiter

def iteritems_unpack(dict the_dict):
    """
    >>> d = {(1,2): (3,4), (5,6): (7,8)}
    >>> iteritems_unpack(d)
    [(1, 2, 3, 4), (5, 6, 7, 8)]
    """
    return sorted([ (a,b,c,d) for (a,b), (c,d) in the_dict.iteritems() ])

def itervalues_unpack(dict the_dict):
    """
    >>> d = {1: (3,4), 2: (7,8)}
    >>> itervalues_unpack(d)
    [(3, 4), (7, 8)]
    """
    return [(a,b) for a,b in the_dict.itervalues() ]
