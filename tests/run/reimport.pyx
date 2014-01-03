# mode: run
# tag: import

# reimports at module init time used to be a problem in Py3
import reimport

def test():
    """
    >>> test()
    True
    """
    import sys
    return reimport in sys.modules.values()
