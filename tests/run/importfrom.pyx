__doc__ = u"""
>>> from distutils import cmd, core, version
>>> import1() == (cmd, core, version)
True
>>> import2() == (cmd, core, version)
True
>>> import3() == (cmd, core, version)
True
>>> import4() == (cmd, core, version)
True
>>> typed_imports()
True
True
an integer is required
Expected type, got int
"""

def import1():
    from distutils import (

        cmd,

core,                    version)
    return cmd, core, version


def import2():
    from distutils import (cmd,

core,


                           version
)
    return cmd, core, version


def import3():
    from distutils import (cmd, core,version)
    return cmd, core, version

def import4():
    from distutils import cmd, core, version
    return cmd, core, version



def typed_imports():

    import sys
    import types
    cdef long maxunicode
    cdef type t
    
    from sys import maxunicode
    print maxunicode == sys.maxunicode
    from types import ModuleType as t
    print t is types.ModuleType

    try:
        from sys import version_info as maxunicode
    except TypeError, e:
        print e

    try:
        from sys import maxunicode as t
    except TypeError, e:
        print e

