# mode: run
# tag: pyclass, getattr

"""
Python bypasses __getattribute__ overrides for some special method lookups.
"""

lookups = []


class PyClass(object):
    """
    >>> del lookups[:]
    >>> obj = PyClass()
    >>> obj.test
    'getattribute(test)'
    >>> lookups
    ['getattribute(test)']
    """
    def __getattribute__(self, name):
        lookup = 'getattribute(%s)' % name
        lookups.append(lookup)
        return lookup

    def __getattr__(self, name):
        lookup = 'getattr(%s)' % name
        lookups.append(lookup)
        return lookup


def use_as_context_manager(obj):
    """
    >>> del lookups[:]
    >>> class PyCM(PyClass):
    ...     def __enter__(self): return '__enter__(%s)' % (self is obj or self)
    ...     def __exit__(self, *args): pass
    >>> obj = PyCM()
    >>> use_as_context_manager(obj)
    '__enter__(True)'
    >>> lookups
    []
    """
    with obj as x:
        pass
    return x
