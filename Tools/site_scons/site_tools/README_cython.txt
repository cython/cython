Howto build cython code with Scons
==================================

Quickstart
----------

My own entry points was [1]. Copy this directory into your project under::
   
   project_root/site_scons/site_tools/

Now add to your top level SConscript::

   env = Environment(PYEXT_USE_DISTUTILS=True)

   env.Tool("pyext")
   env.Tool("cython")

You can now build Cython Extensions using the PythonExtension builder::

   env.PythonExtension("blah", ["blah.pyx"])

The builder is aware of cython dependencies residing in the search paths
given by CYTHONPATH. Dependency tracking is then automatically done by scons.

[1] http://www.mail-archive.com/cython-dev@codespeak.net/msg09540.html

Configuration
-------------

The builders define some configuration variables which you can set like so::

   env.Append(CYTHONPATH = ["thisdirectory"]) # add a directory to cythons search path

Have a look at cython.py and pyext.py for finding them.



-- vim:ft=rst
