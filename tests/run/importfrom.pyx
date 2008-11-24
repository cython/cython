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
