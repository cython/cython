# mode: run
# tag: nogil, withgil, exceptions

cdef void foo_nogil(int i) except * nogil:
    if i != 0: raise ValueError("huhu !")


cdef void foo(int i) except * with gil:
    if i != 0: raise ValueError


cdef int bar(int i) except? -1 with gil:
    if i != 0: raise ValueError
    return 0


cdef int spam(int i) except? -1 with gil:
    if i != 0: raise TypeError
    return -1


def test_foo_nogil():
    """
    >>> test_foo_nogil()
    """
    #
    foo_nogil(0)
    foo_nogil(0)
    with nogil:
        foo_nogil(0)
        foo_nogil(0)
    #
    try:
        with nogil:
            foo_nogil(0)
    finally:
        pass
    #
    try:
        with nogil:
            foo_nogil(0)
        with nogil:
            foo_nogil(0)
    finally:
        pass
    #
    try:
        with nogil:
            foo_nogil(0)
        with nogil:
            foo_nogil(1)
    except:
        with nogil:
            foo_nogil(0)
    finally:
        with nogil:
            foo_nogil(0)
        pass
    #
    try:
        with nogil:
            foo_nogil(0)
            foo_nogil(0)
    finally:
        pass
    #
    try:
        with nogil:
            foo_nogil(0)
            foo_nogil(1)
    except:
        with nogil:
            foo_nogil(0)
    finally:
        with nogil:
            foo_nogil(0)
        pass
    #
    try:
        with nogil:
            foo_nogil(0)
        try:
            with nogil:
                foo_nogil(1)
        except:
            with nogil:
                foo_nogil(1)
        finally:
            with nogil:
                foo_nogil(0)
            pass
    except:
        with nogil:
            foo_nogil(0)
    finally:
        with nogil:
            foo_nogil(0)
        pass
    #
    try:
        with nogil:
            foo_nogil(0)
        try:
            with nogil:
                foo_nogil(1)
        except:
            with nogil:
                foo_nogil(1)
        finally:
            with nogil:
                foo_nogil(1)
            pass
    except:
        with nogil:
            foo_nogil(0)
    finally:
        with nogil:
            foo_nogil(0)
        pass
    #


def test_foo():
    """
    >>> test_foo()
    """
    #
    foo(0)
    foo(0)
    with nogil:
        foo(0)
        foo(0)
    #
    try:
        with nogil:
            foo(0)
    finally:
        pass
    #
    try:
        with nogil:
            foo(0)
        with nogil:
            foo(0)
    finally:
        pass
    #
    try:
        with nogil:
            foo(0)
        with nogil:
            foo(1)
    except:
        with nogil:
            foo(0)
    finally:
        with nogil:
            foo(0)
        pass
    #
    try:
        with nogil:
            foo(0)
            foo(0)
    finally:
        pass
    #
    try:
        with nogil:
            foo(0)
            foo(1)
    except:
        with nogil:
            foo(0)
    finally:
        with nogil:
            foo(0)
        pass
    #
    try:
        with nogil:
            foo(0)
        try:
            with nogil:
                foo(1)
        except:
            with nogil:
                foo(1)
        finally:
            with nogil:
                foo(0)
            pass
    except:
        with nogil:
            foo(0)
    finally:
        with nogil:
            foo(0)
        pass
    #
    try:
        with nogil:
            foo(0)
        try:
            with nogil:
                foo(1)
        except:
            with nogil:
                foo(1)
        finally:
            with nogil:
                foo(1)
            pass
    except:
        with nogil:
            foo(0)
    finally:
        with nogil:
            foo(0)
        pass
    #


def test_bar():
    """
    >>> test_bar()
    """
    #
    bar(0)
    bar(0)
    with nogil:
        bar(0)
        bar(0)
    #
    try:
        with nogil:
            bar(0)
    finally:
        pass
    #
    try:
        with nogil:
            bar(0)
        with nogil:
            bar(0)
    finally:
        pass
    #
    try:
        with nogil:
            bar(0)
        with nogil:
            bar(1)
    except ValueError:
        with nogil:
            bar(0)
    finally:
        with nogil:
            bar(0)
        pass
    #
    try:
        with nogil:
            bar(0)
            bar(0)
    finally:
        pass
    #
    try:
        with nogil:
            bar(0)
            bar(1)
    except ValueError:
        with nogil:
            bar(0)
    finally:
        with nogil:
            bar(0)
        pass
    #
    try:
        with nogil:
            bar(0)
        try:
            with nogil:
                bar(1)
        except ValueError:
            with nogil:
                bar(1)
        finally:
            with nogil:
                bar(0)
            pass
    except ValueError:
        with nogil:
            bar(0)
    finally:
        with nogil:
            bar(0)
        pass
    #
    try:
        with nogil:
            bar(0)
        try:
            with nogil:
                bar(1)
        except ValueError:
            with nogil:
                bar(1)
        finally:
            with nogil:
                bar(1)
            pass
    except ValueError:
        with nogil:
            bar(0)
    finally:
        with nogil:
            bar(0)
        pass
    #

def test_spam():
    """
    >>> test_spam()
    """
    #
    spam(0)
    spam(0)
    with nogil:
        spam(0)
        spam(0)
    #
    try:
        with nogil:
            spam(0)
    finally:
        pass
    #
    try:
        with nogil:
            spam(0)
        with nogil:
            spam(0)
    finally:
        pass
    #
    try:
        with nogil:
            spam(0)
        with nogil:
            spam(1)
    except TypeError:
        with nogil:
            spam(0)
    finally:
        with nogil:
            spam(0)
        pass
    #
    try:
        with nogil:
            spam(0)
            spam(0)
    finally:
        pass
    #
    try:
        with nogil:
            spam(0)
            spam(1)
    except TypeError:
        with nogil:
            spam(0)
    finally:
        with nogil:
            spam(0)
        pass
    #
    try:
        with nogil:
            spam(0)
        try:
            with nogil:
                spam(1)
        except TypeError:
            with nogil:
                spam(1)
        finally:
            with nogil:
                spam(0)
            pass
    except TypeError:
        with nogil:
            spam(0)
    finally:
        with nogil:
            spam(0)
        pass
    #
    try:
        with nogil:
            spam(0)
        try:
            with nogil:
                spam(1)
        except TypeError:
            with nogil:
                spam(1)
        finally:
            with nogil:
                spam(1)
            pass
    except TypeError:
        with nogil:
            spam(0)
    finally:
        with nogil:
            spam(0)
        pass
    #
