.. TODO: Rewrite this to be more comprehensive, with examples!

****************************
Source Files and Compilation
****************************

Cython source file names consist of the name of the module followed by a
``.pyx`` extension, for example a module called primes would have a source
file named :file:`primes.pyx`.

If your module is destined to live in a package, the source file name should
include the full dotted name that the module will eventually have. For
example, a module called primes that will be installed in a package called
numbers should have a source file called numbers.primes.pyx. This will ensure
that the :attr:`__name__` properties of the module and any classes defined in
it are set correctly. If you don't do this, you may find that pickling doesn't
work, among other problems. It also ensures that the Cython compiler has the
right idea about the layout of the module namespace, which can be important
when accessing extension types defined in other modules.

Once you have written your ``.pyx`` file, there are a couple of ways of turning it
into an extension module. One way is to compile it manually with the Cython
compiler, e.g.::

    $ cython primes.pyx

This will produce a file called :file:`primes.c`, which then needs to be
compiled with the C compiler using whatever options are appropriate on your
platform for generating an extension module. There's a Makefile in the Demos
directory (called Makefile.nodistutils) that shows how to do this for Linux.

The other, and probably better, way is to use the :mod:`distutils` extension
provided with Cython. See the :file:`setup.py` file in the Demos directory for an
example of how to use it. This method has the advantage of being
cross-platform -- the same setup file should work on any platform where
:mod:`distutils` can compile an
extension module.
