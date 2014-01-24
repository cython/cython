# mode: run
# tag: control-flow, uninitialized

def conditional(cond):
    """
    >>> conditional(True)
    []
    >>> conditional(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    if cond:
        a = []
    return a

def inside_loop(iter):
    """
    >>> inside_loop([1,2,3])
    3
    >>> inside_loop([])
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'i' referenced before assignment
    """
    for i in iter:
        pass
    return i

def try_except(cond):
    """
    >>> try_except(True)
    []
    >>> try_except(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    try:
        if cond:
            a = []
        raise ValueError
    except ValueError:
        return a

def try_finally(cond):
    """
    >>> try_finally(True)
    []
    >>> try_finally(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    try:
        if cond:
            a = []
        raise ValueError
    finally:
        return a

def deleted(cond):
    """
    >>> deleted(False)
    {}
    >>> deleted(True)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    a = {}
    if cond:
        del a
    return a

def test_nested(cond):
    """
    >>> test_nested(True)
    >>> test_nested(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    if cond:
        def a():
            pass
    return a()

def test_outer(cond):
    """
    >>> test_outer(True)
    {}
    >>> test_outer(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    if cond:
        a = {}
    def inner():
        return a
    return a

def test_inner(cond):
    """
    >>> test_inner(True)
    {}
    >>> test_inner(False)
    Traceback (most recent call last):
    ...
    NameError: free variable 'a' referenced before assignment in enclosing scope
    """
    if cond:
        a = {}
    def inner():
        return a
    return inner()

def test_class(cond):
    """
    >>> test_class(True)
    1
    >>> test_class(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'A' referenced before assignment
    """
    if cond:
        class A:
            x = 1
    return A.x


def test_try_except_regression(c):
    """
    >>> test_try_except_regression(True)
    (123,)
    >>> test_try_except_regression(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    if c:
        a = (123,)
    try:
        return a
    except:
        return a


def test_try_finally_regression(c):
    """
    >>> test_try_finally_regression(True)
    (123,)
    >>> test_try_finally_regression(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'a' referenced before assignment
    """
    if c:
        a = (123,)
    try:
        return a
    finally:
        return a


def test_expression_calculation_order_bug(a):
    """
    >>> test_expression_calculation_order_bug(False)
    []
    >>> test_expression_calculation_order_bug(True)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable 'b' referenced before assignment
    """
    if not a:
        b = []
    return (a or b) and (b or a)
