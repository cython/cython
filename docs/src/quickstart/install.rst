.. _install:

Installing Cython
=================

Many scientific Python distributions, such as Anaconda [Anaconda]_,
Enthought Canopy [Canopy]_, and Sage [Sage]_,
bundle Cython and no setup is needed.  Note however that if your
distribution ships a version of Cython which is too old you can still
use the instructions below to update Cython.  Everything in this
tutorial should work with Cython 0.11.2 and newer, unless a footnote
says otherwise.

Unlike most Python software, Cython requires a C compiler to be
present on the system. The details of getting a C compiler varies
according to the system used:

 - **Linux** The GNU C Compiler (gcc) is usually present, or easily
   available through the package system. On Ubuntu or Debian, for
   instance, the command ``sudo apt-get install build-essential`` will
   fetch everything you need.

 - **Mac OS X** To retrieve gcc, one option is to install Apple's
   XCode, which can be retrieved from the Mac OS X's install DVDs or
   from https://developer.apple.com/.

 - **Windows** A popular option is to use the open source MinGW (a
   Windows distribution of gcc). See the appendix for instructions for
   setting up MinGW manually. Enthought Canopy and Python(x,y) bundle
   MinGW, but some of the configuration steps in the appendix might
   still be necessary.  Another option is to use Microsoft's Visual C.
   One must then use the same version which the installed Python was
   compiled with.

.. dagss tried other forms of ReST lists and they didn't look nice
.. with rst2latex.

The simplest way of installing Cython is by using ``pip``::

  pip install Cython


The newest Cython release can always be downloaded from
http://cython.org.  Unpack the tarball or zip file, enter the
directory, and then run::

  python setup.py install


For one-time builds, e.g. for CI/testing, on platforms that are not covered
by one of the wheel packages provided on PyPI, it is substantially faster
than a full source build to install an uncompiled (slower) version of Cython
with

::

    pip install Cython --install-option="--no-cython-compile"


.. [Anaconda] https://docs.anaconda.com/anaconda/
.. [Canopy] https://www.enthought.com/product/canopy/
.. [Sage] W. Stein et al., Sage Mathematics Software, http://www.sagemath.org/
