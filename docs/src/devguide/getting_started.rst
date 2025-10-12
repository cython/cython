.. _Getting Started:

Getting started working on Cython
=================================

Git
---

Cython is currently hosted `on GitHub <https://github.com/cython/cython/>`_ and uses Git to track changes to
the source code.  The majority of development happens on the "master" branch, but we typically maintain one or
two stable release branches which are updated with bugfixes.  Changes that go into the main Cython repository should
never make the branch unreleasable (even if minor breakages can happen from time to time).

To get started working with Cython's code, you will need `git <https://git-scm.com/downloads>`_
to create a local clone of the repository.

The typical workflow on Github is to `fork the code <https://github.com/cython/cython/fork>`_,
creating a repository in your own Github account named ``github.com/<your_user_name>/cython``.

To then clone the repository to your local machine run:

.. code-block:: bash

    git clone git@github.com:<your_user_name>/cython.git
    cd cython

If you want to work on a specific feature, then create a branch for that feature on your local PC and check
it out:

.. code-block:: bash

    git checkout -b from-future-import-braces

When you have finished working on your feature you can commit the changes locally, and then push it to your
personal Github copy of Cython:

.. code-block:: bash

    git commit -a  # commit all changed files
    git push origin from-future-import-braces

You can then create a pull request using the Github web interface to merge your branch into the main Cython
repository.


Running Cython on your PC
-------------------------

When developing Cython itself you do not need to compile or install it.  (Cython can optionally be compiled
for speed reasons, but when working on it it is usually easier not to.)  Cython itself is designed to have
no dependencies to run (outside the Python standard library) so no preparation or virtual environments are
usually necessary.  However some specific features or tests do have runtime requirements. These are usually
installable from the ``test-requirements.txt`` file.

To run Cython for development, simply check out the
Cython repository as described above, change to that directory and run:

.. code-block:: bash

    python3 cython.py <path/to/some/file>.pyx

This runs Cython on some small test file that you're interested in.  If you want to compile the
generated C code too, then the ``cythonize`` command can do that for you:

.. code-block:: bash

    python3 cythonize.py -if <path/to/some/file>.pyx

This is usually the easiest way to develop.  However, sometimes it's useful to investigate
a Cython issue when dealing with a larger third-party package.  In this case, create a
virtual environment and activate it:

.. code-block:: bash

    python3 -m venv your_venv
    source your_venv/bin/activate  # on Windows this is "scripts/activate"

(or use any preferred tool you have).  Change to the checked-out Cython repo directory and
install Cython in editable mode using:

.. code-block:: bash

    NO_CYTHON_COMPILE=true pip install -e .

and then use that virtual environment.
