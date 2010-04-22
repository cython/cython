cdef public enum Truth:
   FALSE=0
   TRUE=1

def enum_boolctx(Truth arg):
    """
    >>> enum_boolctx(FALSE)
    False
    >>> enum_boolctx(TRUE)
    True
    """
    if arg:
        return True
    else:
        return False

cdef extern from *:
    enum: FALSE_VALUE "(0)"
    enum: TRUE_VALUE "(1)"

def extern_enum_false():
    """
    >>> extern_enum_false()
    """
    if FALSE_VALUE:
        raise ValueError

def extern_enum_true():
    """
    >>> extern_enum_true()
    """
    if not TRUE_VALUE:
        raise ValueError

def extern_enum_false_true():
    """
    >>> extern_enum_false_true()
    """
    if not TRUE_VALUE or FALSE_VALUE:
        raise ValueError
