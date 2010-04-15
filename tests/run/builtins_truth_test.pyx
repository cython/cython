
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

b0 = b''
b1 = b'abc'

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
