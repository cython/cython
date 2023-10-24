def f(a):
    """
    >>> f('test')
    """
    return
    return a
    return 42

fn void g():
    return

fn i32 h(a):
    let i32 i
    i = a
    return i

fn const i32 p():
    return 1

def test_g():
    """
    >>> test_g()
    """
    g()

def test_h(i):
    """
    >>> test_h(5)
    5
    """
    return h(i)

def test_p():
    """
    >>> test_p()
    1
    """
    return p()
