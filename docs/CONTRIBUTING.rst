Welcome, and thank you for your interest in contributing!
=========================================================

If you are looking for a good way to contribute to the Cython project, please

* have a look at the `Cython Hacker Guide <https://github.com/cython/cython/wiki/HackerGuide>`_,
  especially the section on `getting started <https://github.com/cython/cython/wiki/HackerGuide#getting-started>`_.
* look through the `issues that need help <https://github.com/cython/cython/labels/help%20wanted>`_.
* look through the `issues that are a good entry point for beginners <https://github.com/cython/cython/labels/good%20first%20issue>`_.
* ask on the `core developers mailing list <https://mail.python.org/mailman/listinfo/cython-devel>`_ for guidance.

Note that some (but not all) "good first issue"s also require an understanding of C
and a bit of the CPython C-API – usually those that also have the ``Code Generation``
label. We generally consider a ticket a "good first issue" if it has a limited scope
that new contributors will have to learn about, e.g. only needs changes to the parser,
the type analysis or the code generation, but does not require changes all across the
compiler pipeline.

If you have code that you want to contribute, please make sure that it

* includes tests in the ``tests/`` directory (see the `Hacker Guide on Testing <https://github.com/cython/cython/wiki/HackerGuide#the-test-suite>`_)
* comes in form of a pull request

We use `github actions <https://github.com/cython/cython/actions>`_ for cross-platform testing, including pull requests.
