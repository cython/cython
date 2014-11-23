# mode: run
# tag: cpp, werror

cdef int raise_TypeError() except *:
    raise TypeError("custom")

cdef extern from "cpp_exceptions_nogil_helper.h" nogil:
    cdef void foo "foo"(int i) except +
    cdef void bar "foo"(int i) except +ValueError
    cdef void spam"foo"(int i) except +raise_TypeError

cdef int foo_nogil(int i) nogil except *:
    foo(i)

def test_foo_nogil():
    """
    >>> test_foo_nogil()
    """
    foo_nogil(0)
    with nogil:
        foo_nogil(0)

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
