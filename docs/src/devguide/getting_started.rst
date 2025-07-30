.. _Getting Started:

The Git Project Repositories
============================

The obvious place to start is the `source repository <https://github.com/cython/cython/>`_ of the master branch
on `github <http://github.com/>`_. The Cython source is kept under `git <http://git-scm.com/>`_ control.
In case you don't want to use git, you can also use `Mercurial <http://hg-git.github.com/>`_.
If you know Subversion or CVS, the most important difference that you need to know about is that
the repository does not just reside on a server with which you have to interact.
Instead, you get the entire repository when you do a checkout.
So you can easily work on your local copy and commit changes (``git commit``) as you see fit,
pull updates from the main repository (``git pull/fetch``, possibly with rebase, see below) and
then collect or select your changes to send them to the mailing list for approval. You can also
clone the repository on github and trigger a pull request to let us review and merge your changes.


*Note*: Do not pull somebody's branch if the name starts with an underscore.
See "Feature branches" section below. In general, only pull somebody's "private" branch
if you really have to, always try to develop off the upstream master.

`cython <https://github.com/cython/cython>`_ is the main development where all the major development work happens.
Changes that go into this repository should never make the branch unreleasable
(even if minor breakages can happen from time to time). The
`latest developer documentation <https://sage.math.washington.edu:8091/hudson/job/cython-docs/doclinks/1/>`_
from the ``docs`` directory is available from our build server.

There are other Cython repositories on github, for example we find it useful for Google Summer of Code students
to have their own repositories which periodically get merged into main when they are ready.
Being a distributed revision control system, anyone is free to host a personal repository elsewhere as well.

A new release typically comes every third month or so.

Feature branches
----------------

For non-trivial new features that may require a long list of commits and a final review in a pull request,
it may be a good idea to use a *rebasable feature branch* (in Mercurial this is known as a "patch queue").
It is like a normal branch, but instead of merging, you rebase:

* Start a feature branch. It is a good idea to keep the name "master" for Cython's master and not make your own changes there.

  .. code-block:: bash

      git checkout -b _myfeature

* Develop and commit...

* You want to merge in upstream master. Now, do a rebase instead:

  .. code-block:: bash

     git checkout master
     git pull upstream master # should fast-forward if you stay off master for your own development
     git checkout _myfeature
     git pull --rebase master # leads you through a sequence of merging individual patches
     git push -f dagss _myfeature # Do a force-push

Finally, when merging feature branches into master, use the ``--no-ff`` flag, so that the feature branch stands out in history.

The advantage of this approach is that merges happen commit by commit. This makes it appear as though you developed
starting from the freshest ``upstream/master``, instead of developing against a moving target.

It is imperative that nobody else has fetched the commits you are rebasing. A rebase recreates all the commits,
and if others also have those commits there will end up being duplicate commits: Commits that are really the same,
but which Git sees as distinct commits.

We are using the convention that branch names should start with an underscore, like ``_mybranch``,
to say "keep off this branch, I may rebase it any moment".

Git tricks
----------

Put this in your .bashrc to get a blue branch name in front of your prompt:

.. code-block:: bash

    # make my prompt "(master) ~/code/cython $ "
    export PS1='\[\e[0;34;49m\]$(__git_ps1 "(%s) ")\[\e[0;0m\]\w $ '

``https://github.com/magit/magit|Magit`` is a nice Emacs plugin for git. The key feature is that it
allows you very easily to stage and commit sets of individual hunks, so that you can leave debug code
in your working tree without any hassle. Some other Git GUIs have the same feature.

