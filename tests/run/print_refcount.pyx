# mode: run
import sys

def test_print_refcount():
    """
    >>> test_print_refcount()
    """
    old_stdout = sys.stdout
    class StdoutGuard:
        def __getattr__(self, attr):
            sys.stdout = old_stdout
            raise RuntimeError
    sys.stdout = StdoutGuard()
    try:
        print "Hello", "world!"
    except RuntimeError:
        pass
    finally:
        sys.stdout = old_stdout
    class TriggerSIGSEGV(object):
        pass

def test_printone_refcount():
    """
    >>> test_printone_refcount()
    """
    old_stdout = sys.stdout
    class StdoutGuard:
        def __getattr__(self, attr):
            sys.stdout = old_stdout
            raise RuntimeError
    sys.stdout = StdoutGuard()
    try:
        print "Oops!"
    except RuntimeError:
        pass
    finally:
        sys.stdout = old_stdout
    class TriggerSIGSEGV(object):
        pass
