def single_except(a, x):
    """
    >>> single_except(ValueError, None)
    2
    >>> single_except(ValueError, ValueError('test'))
    3
    >>> single_except(ValueError, TypeError('test'))
    Traceback (most recent call last):
    TypeError: test
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
        i = 2
    except a:
        i = 3
    return i

def single_except_builtin(a, x):
    """
    >>> single_except_builtin(ValueError, None)
    2
    >>> single_except_builtin(ValueError, ValueError('test'))
    3
    >>> single_except_builtin(ValueError, TypeError('test'))
    Traceback (most recent call last):
    TypeError: test
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
        i = 2
    except ValueError:
        i = 3
    return i

def single_except_expression(a, x):
    """
    >>> single_except_expression([[ValueError]], None)
    2
    >>> single_except_expression([[ValueError]], ValueError('test'))
    3
    >>> single_except_expression([[ValueError]], TypeError('test'))
    Traceback (most recent call last):
    TypeError: test
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
        i = 2
    except a[0][0]:
        i = 3
    return i


exceptions = (ValueError, TypeError)


def single_except_global_tuple(x):
    """
    >>> single_except_global_tuple(None)
    2
    >>> single_except_global_tuple(ValueError('test'))
    3
    >>> single_except_global_tuple(TypeError('test'))
    3
    >>> class TypeErrorSubtype(TypeError): pass
    >>> single_except_global_tuple(TypeErrorSubtype('test'))
    3
    >>> single_except_global_tuple(AttributeError('test'))
    Traceback (most recent call last):
    AttributeError: test
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
        i = 2
    except exceptions:
        i = 3
    return i


def double_except_no_raise(a,b):
    """
    >>> double_except_no_raise(TypeError, ValueError)
    1
    """
    d = a or b  # mark used

    cdef int i
    try:
        i = 1
    except a:
        i = 2
    except b:
        i = 3
    return i

def double_except_raise(x, a, b):
    """
    >>> double_except_raise(None, TypeError, ValueError)
    1
    >>> double_except_raise(TypeError('test'), TypeError, ValueError)
    2
    >>> double_except_raise(ValueError('test'), TypeError, ValueError)
    3
    >>> double_except_raise(None, TypeError, ValueError)
    1
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
    except a:
        i = 2
    except b:
        i = 3
    return i

def target_except_no_raise(a):
    """
    >>> target_except_no_raise(TypeError)
    1
    """
    d = a  # mark used

    cdef int i
    try:
        i = 1
    except a, b:
        i = 2
    return i

def target_except_raise(x, a):
    """
    >>> target_except_raise(None, TypeError)
    1
    >>> target_except_raise(TypeError('test'), TypeError)
    2
    >>> target_except_raise(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> target_except_raise(None, TypeError)
    1
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
    except a, b:
        i = 2
        assert isinstance(b, a)
    return i

def tuple_except_builtin(x):
    """
    >>> tuple_except_builtin(None)
    1
    >>> tuple_except_builtin(TypeError('test'))
    2
    >>> tuple_except_builtin(ValueError('test'))
    2
    >>> tuple_except_builtin(IndexError('5'))
    Traceback (most recent call last):
    IndexError: 5
    >>> tuple_except_builtin(None)
    1
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
    except (TypeError, ValueError):
        i = 2
    return i

def normal_and_bare_except_no_raise(a):
    """
    >>> normal_and_bare_except_no_raise(TypeError)
    1
    """
    d = a  # mark used

    cdef int i
    try:
        i = 1
    except a:
        i = 2
    except:
        i = 3
    return i

def normal_and_bare_except_raise(x, a):
    """
    >>> normal_and_bare_except_raise(None, TypeError)
    1
    >>> normal_and_bare_except_raise(TypeError('test'), TypeError)
    2
    >>> normal_and_bare_except_raise(ValueError('test'), TypeError)
    3
    >>> normal_and_bare_except_raise(TypeError('test'), (TypeError, ValueError))
    2
    >>> normal_and_bare_except_raise(ValueError('test'), (TypeError, ValueError))
    2
    >>> normal_and_bare_except_raise(None, TypeError)
    1
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
    except a:
        i = 2
    except:
        i = 3
    return i

def tuple_except_index_target_no_raise(a, b, c):
    """
    >>> l = [None, None]
    >>> tuple_except_index_target_no_raise(TypeError, ValueError, l)
    1
    >>> l
    [None, None]
    """
    d = a or b or c  # mark used

    cdef int i
    try:
        i = 1
    except (a, b), c[1]:
        i = 2
    return i

def tuple_except_index_target_raise(x, a, b, c):
    """
    >>> l = [None, None]
    >>> tuple_except_index_target_raise(None, TypeError, ValueError, l)
    1
    >>> l
    [None, None]
    >>> tuple_except_index_target_raise(TypeError('test'), TypeError, ValueError, l)
    2
    >>> l[0] is None, isinstance(l[1], TypeError)
    (True, True)
    >>> tuple_except_index_target_raise(ValueError('test'), TypeError, ValueError, l)
    2
    >>> l[0] is None, isinstance(l[1], ValueError)
    (True, True)
    >>> tuple_except_index_target_raise(IndexError('5'), TypeError, ValueError, l)
    Traceback (most recent call last):
    IndexError: 5
    >>> tuple_except_index_target_raise(None, TypeError, ValueError, l)
    1
    >>> l[0] is None, isinstance(l[1], ValueError)
    (True, True)
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
    except (a, b), c[1]:
        i = 2
        assert isinstance(c[1], (a,b))
    return i

def loop_bare_except_no_raise(a, b, int c):
    """
    >>> loop_bare_except_no_raise(TypeError, range(2), 2)
    (1, 3528)
    """
    cdef int i = 1
    for a in b:
        try:
            c = c * 42
        except:
            i = 17
    return i,c

def loop_bare_except_raise(a, b, int c):
    """
    >>> loop_bare_except_raise(TypeError, range(2), 2)
    (1, 3528)
    >>> loop_bare_except_raise(TypeError, range(3), 2)
    (17, 148176)
    >>> loop_bare_except_raise(TypeError, range(4), 2)
    (17, 6223392)
    """
    cdef int i = 1
    for a in b:
        try:
            c = c * 42
            if a == 2:
                raise TypeError('test')
        except:
            i = 17
    return i,c

def bare_except_reraise_no_raise(l):
    """
    >>> l = [None]
    >>> bare_except_reraise_no_raise(l)
    1
    >>> l
    [None]
    """
    d = l  # mark used

    cdef int i
    try:
        i = 1
    except:
        l[0] = 2
        raise
    return i

def bare_except_reraise_raise(x, l):
    """
    >>> l = [None]
    >>> bare_except_reraise_raise(None, l)
    1
    >>> l
    [None]
    >>> bare_except_reraise_raise(TypeError('test'), l)
    Traceback (most recent call last):
    TypeError: test
    >>> l
    [2]
    >>> l = [None]
    >>> bare_except_reraise_raise(None, l)
    1
    >>> l
    [None]
    """
    cdef int i
    try:
        i = 1
        if x:
            raise x
    except:
        l[0] = 2
        raise
    return i

def except_as_no_raise(a):
    """
    >>> except_as_no_raise(TypeError)
    1
    """
    d = a  # mark used

    try:
        i = 1
    except a as b:
        i = 2
    return i

def except_as_raise(x, a):
    """
    >>> except_as_raise(None, TypeError)
    1
    >>> except_as_raise(TypeError('test'), TypeError)
    2
    >>> except_as_raise(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> except_as_raise(None, TypeError)
    1
    """
    try:
        i = 1
        if x:
            raise x
    except a as b:
        i = 2
        assert isinstance(b, a)
    return i

def except_as_no_raise_does_not_touch_target(a):
    """
    >>> i,b = except_as_no_raise_does_not_touch_target(TypeError)
    >>> i
    1
    >>> b
    1
    """
    d = a  # mark used

    b = 1
    try:
        i = 1
    except a as b:
        i = 2
    return i, b

def except_as_raise_does_not_delete_target(x, a):
    """
    >>> except_as_raise_does_not_delete_target(None, TypeError)
    1
    >>> except_as_raise_does_not_delete_target(TypeError('test'), TypeError)
    2
    >>> except_as_raise_does_not_delete_target(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> except_as_raise_does_not_delete_target(None, TypeError)
    1
    """
    b = 1
    try:
        i = 1
        if x:
            raise x
    except a as b:
        i = 2
        assert isinstance(b, a)

    # exception variable leaks with Py2 except-as semantics
    if x:
        assert isinstance(b, a)
    else:
        assert b == 1
    return i

def except_as_raise_with_empty_except(x, a):
    """
    >>> except_as_raise_with_empty_except(None, TypeError)
    >>> except_as_raise_with_empty_except(TypeError('test'), TypeError)
    >>> except_as_raise_with_empty_except(ValueError('test'), TypeError)
    Traceback (most recent call last):
    ValueError: test
    >>> except_as_raise_with_empty_except(None, TypeError)
    """
    try:
        if x:
            raise x
        b = 1
    except a as b:
        pass
    if x:
        assert isinstance(b, a)
    else:
        assert b == 1

def complete_except_as_no_raise(a, b):
    """
    >>> complete_except_as_no_raise(TypeError, ValueError)
    5
    """
    d = a or b  # mark used

    try:
        i = 1
    except (a, b) as c:
        i = 2
    except (b, a) as c:
        i = 3
    except:
        i = 4
    else:
        i = 5
    return i

def complete_except_as_raise(x, a, b):
    """
    >>> complete_except_as_raise(None, TypeError, ValueError)
    5
    >>> complete_except_as_raise(TypeError('test'), TypeError, ValueError)
    2
    >>> complete_except_as_raise(ValueError('test'), TypeError, ValueError)
    2
    >>> complete_except_as_raise(IndexError('5'), TypeError, ValueError)
    4
    >>> complete_except_as_raise(None, TypeError, ValueError)
    5
    """
    try:
        i = 1
        if x:
            raise x
    except (a, b) as c:
        i = 2
        assert isinstance(c, (a, b))
    except (b, a) as c:
        i = 3
        assert isinstance(c, (a, b))
    except:
        i = 4
    else:
        i = 5
    return i
