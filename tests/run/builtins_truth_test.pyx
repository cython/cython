
def bool_list(list obj):
    """
    >>> bool_list( [] )
    False
    >>> bool_list( [1] )
    True
    >>> bool_list(None)
    False
    """
    return bool(obj)


def if_list(list obj):
    """
    >>> if_list( [] )
    False
    >>> if_list( [1] )
    True
    >>> if_list(None)
    False
    """
    if obj:
        return True
    else:
        return False


def if_list_nogil(list obj):
    """
    >>> if_list_nogil( [] )
    False
    >>> if_list_nogil( [1] )
    True
    >>> if_list_nogil(None)
    False
    """
    cdef bint result
    with nogil:
        if obj:
            result = True
        else:
            result = False
    return result


def if_list_literal(t):
    """
    >>> if_list_literal(True)
    True
    >>> if_list_literal(False)
    False
    """
    if t:
        if [1,2,3]:
            return True
        else:
            return False
    else:
        if []:
            return True
        else:
            return False


def bool_tuple(tuple obj):
    """
    >>> bool_tuple( () )
    False
    >>> bool_tuple( (1,) )
    True
    >>> bool_tuple(None)
    False
    """
    return bool(obj)


def if_tuple(tuple obj):
    """
    >>> if_tuple( () )
    False
    >>> if_tuple( (1,) )
    True
    >>> if_tuple(None)
    False
    """
    if obj:
        return True
    else:
        return False


def if_tuple_literal(t):
    """
    >>> if_tuple_literal(True)
    True
    >>> if_tuple_literal(False)
    False
    """
    if t:
        if (1,2,3):
            return True
        else:
            return False
    else:
        if ():
            return True
        else:
            return False


def bool_set(set obj):
    """
    >>> bool_set( set() )
    False
    >>> bool_set( set([1]) )
    True
    >>> bool_set(None)
    False
    """
    return bool(obj)


def if_set(set obj):
    """
    >>> if_set( set() )
    False
    >>> if_set( set([1]) )
    True
    >>> if_set(None)
    False
    """
    if obj:
        return True
    else:
        return False


def if_set_nogil(set obj):
    """
    >>> if_set_nogil( set() )
    False
    >>> if_set_nogil( set([1]) )
    True
    >>> if_set_nogil(None)
    False
    """
    cdef bint result
    with nogil:
        if obj:
            result = True
        else:
            result = False
    return result


def if_set_literal(t):
    """
    >>> if_set_literal(True)
    True
    >>> if_set_literal(False)
    False
    """
    if t:
        if {1,2,3}:
            return True
        else:
            return False
    else:
        if set():
            return True
        else:
            return False


def bool_frozenset(frozenset obj):
    """
    >>> bool_frozenset( frozenset() )
    False
    >>> bool_frozenset( frozenset([1]) )
    True
    >>> bool_frozenset(None)
    False
    """
    return bool(obj)


def if_frozenset(frozenset obj):
    """
    >>> if_frozenset( frozenset() )
    False
    >>> if_frozenset( frozenset([1]) )
    True
    >>> if_frozenset(None)
    False
    """
    if obj:
        return True
    else:
        return False


b0 = b''
b1 = b'abc'

def bool_bytes(bytes obj):
    """
    >>> bool_bytes(b0)
    False
    >>> bool_bytes(b1)
    True
    >>> bool_bytes(None)
    False
    """
    return bool(obj)

def if_bytes(bytes obj):
    """
    >>> if_bytes(b0)
    False
    >>> if_bytes(b1)
    True
    >>> if_bytes(None)
    False
    """
    if obj:
        return True
    else:
        return False

def if_bytes_literal(t):
    """
    >>> if_bytes_literal(True)
    True
    >>> if_bytes_literal(False)
    False
    """
    if t:
        if b'abc':
            return True
        else:
            return False
    else:
        if b'':
            return True
        else:
            return False


u0 = u''
u1 = u'abc'

def bool_unicode(unicode obj):
    """
    >>> bool_unicode(u0)
    False
    >>> bool_unicode(u1)
    True
    >>> bool_unicode(None)
    False
    """
    return bool(obj)

def if_unicode(unicode obj):
    """
    >>> if_unicode(u0)
    False
    >>> if_unicode(u1)
    True
    >>> if_unicode(None)
    False
    """
    if obj:
        return True
    else:
        return False

def if_unicode_literal(t):
    """
    >>> if_unicode_literal(True)
    True
    >>> if_unicode_literal(False)
    False
    """
    if t:
        if u'abc':
            return True
        else:
            return False
    else:
        if u'':
            return True
        else:
            return False
