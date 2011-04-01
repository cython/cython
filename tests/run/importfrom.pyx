from distutils import cmd, core, version

def import1():
    """
    >>> import1() == (cmd, core, version)
    True
    """
    from distutils import (

        cmd,

core,                    version)
    return cmd, core, version


def import2():
    """
    >>> import2() == (cmd, core, version)
    True
    """
    from distutils import (cmd,

core,


                           version
)
    return cmd, core, version


def import3():
    """
    >>> import3() == (cmd, core, version)
    True
    """
    from distutils import (cmd, core,version)
    return cmd, core, version

def import4():
    """
    >>> import4() == (cmd, core, version)
    True
    """
    from distutils import cmd, core, version
    return cmd, core, version



def typed_imports():
    """
    >>> typed_imports()
    True
    True
    an integer is required
    Expected type, got int
    """

    import sys
    import types
    cdef long maxunicode
    cdef type t

    from sys import maxunicode
    print(maxunicode == sys.maxunicode)
    from types import ModuleType as t
    print(t is types.ModuleType)

    try:
        from sys import version_info as maxunicode
    except TypeError, e:
        print(e)

    try:
        from sys import maxunicode as t
    except TypeError, e:
        print(e)
