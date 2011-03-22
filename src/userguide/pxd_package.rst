I think this is a result of a recent change to Pyrex that
has been merged into Cython.

If a directory contains an :file:`__init__.py` or :file:`__init__.pyx` file,
it's now assumed to be a package directory. So, for example,
if you have a directory structure::

   foo/
     __init__.py
     shrubbing.pxd
     shrubbing.pyx

then the shrubbing module is assumed to belong to a package
called 'foo', and its fully qualified module name is
'foo.shrubbing'.

So when Pyrex wants to find out whether there is a `.pxd` file for shrubbing,
it looks for one corresponding to a module called `foo.shrubbing`. It
does this by searching the include path for a top-level package directory
called 'foo' containing a file called 'shrubbing.pxd'.

However, if foo is the current directory you're running
the compiler from, and you haven't added foo to the
include path using a -I option, then it won't be on
the include path, and the `.pxd` won't be found.

What to do about this depends on whether you really
intend the module to reside in a package.

If you intend shrubbing to be a top-level module, you
will have to move it somewhere else where there is
no :file:`__init__.*` file.

If you do intend it to reside in a package, then there
are two alternatives:

1. cd to the directory containing foo and compile
   from there::

      cd ..; cython foo/shrubbing.pyx

2. arrange for the directory containing foo to be
   passed as a -I option, e.g.::

      cython -I .. shrubbing.pyx

Arguably this behaviour is not very desirable, and I'll
see if I can do something about it.

