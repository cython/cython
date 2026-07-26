Bug/Feature Tracking and Project Culture
========================================

The Cython project is strongly driven by interest and has a rather free and open development culture.
There are a couple of main developers and regular committers from various different backgrounds,
but we are very happy to receive input and patches from everyone.

In order try to keep the intervals between releases short, however, there are a couple of restrictions that we impose on ourselves,
especially when working on bug-fix (third digit) releases.

1. Every change that goes into a bug fix release must be backed by a `ticket <https://github.com/cython/cython/issues>`_.

2. Every ticket should have a bug test case associated with it. Fairly often, users who report a problem add an example
   to the ticket description anyway, but it definitely makes the life of the developers easier when they do so in form
   of a readily usable test case. Otherwise, the developers have to write it up themselves, in addition to fixing the bug.
   Please see the section about :ref:`The Test Suite` below to find out how to write a good test.

   Either way, before a ticket gets fixed or assigned a milestone, there must be a failing test
   case in the appropriate ``tests/`` directory (preferably ``tests/run``) that is named 
   "``nicely_descriptive_name_here_Txyz.pyx``" (where ``'xyz'`` is the ticket number).
   Please try to do this even for the tricky cases that feel like there isn't a good test case.
   Reproducing a bug is critical for fixing it, and having a test case is critical for knowing when
   it's fixed and for not breaking it in the future. Broken examples are listed in the ``tests/bugs.txt``
   file, and are skipped during normal testing (this makes it easier to detect regressions when doing other work).

3. A working patch in a pull request, together with a descriptive test, will definitely accelerate the
   mainline bug fixing. If you are unsure where to get started, it's usually best to ask on the mailing list before getting lost.

4. Pull requests will usually be handled with priority and should at least receive a timely review.

