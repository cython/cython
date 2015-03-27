
def pylong_join(count, digits_ptr='digits', join_type='unsigned long'):
    """
    Generate an unrolled shift-then-or loop over the first 'count' digits.
    Assumes that they fit into 'join_type'.
    """
    return ('(' * (count * 2) + "(%s)" % join_type + ' | '.join(
        "%s[%d])%s)" % (digits_ptr, _i, " << PyLong_SHIFT" if _i else '')
        for _i in range(count-1, -1, -1)))
