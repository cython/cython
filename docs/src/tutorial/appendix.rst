Appendix: Installing MinGW on Windows
=====================================

 1. Download the MinGW installer from
    http://www.mingw.org/wiki/HOWTO_Install_the_MinGW_GCC_Compiler_Suite.
    (As of this
    writing, the download link is a bit difficult to find; it's under
    "About" in the menu on the left-hand side). You want the file
    entitled "Automated MinGW Installer" (currently version 5.1.4).
 2. Run it and install MinGW. Only the basic package is strictly
    needed for Cython, although you might want to grab at least the
    C++ compiler as well.
 3. You need to set up Windows' "PATH" environment variable so that
    includes e.g. "c:\\mingw\\bin" (if you installed MinGW to
    "c:\\mingw"). The following web-page describes the procedure
    in Windows XP (the Vista procedure is similar):
    https://support.microsoft.com/kb/310519
 4. Finally, tell Python to use MinGW as the default compiler
    (otherwise it will try for Visual C). If Python is installed to
    "c:\\Python27", create a file named
    "c:\\Python27\\Lib\\distutils\\distutils.cfg" containing::

      [build]
      compiler = mingw32

The [WinInst]_ wiki page contains updated information about this
procedure. Any contributions towards making the Windows install
process smoother is welcomed; it is an unfortunate fact that none of
the regular Cython developers have convenient access to Windows.

Python 3.8+
-----------

Since Python 3.8, the search paths of DLL dependencies has been reset. ([changelog]_)

Only the system paths, the directory containing the DLL or PYD file
are searched for load-time dependencies.
Instead, a new function [os.add_dll_directory]_ was added for additional
search path. But this runtime patch is not useful when distribution.

Unlike MSVC, MinGW has its owned standard libraries such as ``libstdc++-6.dll``,
which are not be placed at system path (like ``C:\Windows\System32``).
You can check the dependencies by MSVC tool ``dumpbin``::

    > dumpbin /dependents my_gnu_extension.cp38-win_amd64.pyd
    ...
    Dump of file my_gnu_extension.cp38-win_amd64.pyd
    
    File Type: DLL
    
      Image has the following dependencies:
      
          python38.dll
          KERNEL32.dll
          msvcrt.dll
          libgcc_s_seh-1.dll
          libstdc++-6.dll
          ...

We can embed standard libraries by static linking,
add those options to linker::

    -static-libgcc -static-libstdc++ -Wl,-Bstatic,--whole-archive -lwinpthread -Wl,--no-whole-archive

In ``setup.py``, a cross platform config can be added through extending ``build_ext`` class::

    from setuptools import setup
    from setuptools.command.build_ext import build_ext

    link_args = ['-static-libgcc',
                 '-static-libstdc++',
                 '-Wl,-Bstatic,--whole-archive',
                 '-lwinpthread',
                 '-Wl,--no-whole-archive']

    ...  # Add extensions

    class Build(build_ext):
        def build_extensions(self):
            if self.compiler.compiler_type == 'mingw32':
                for e in self.extensions:
                    e.extra_link_args = link_args
            super(Build, self).build_extensions()

    setup(
        ...
        cmdclass={'build_ext': Build},
        ...
    )

.. [WinInst] https://github.com/cython/cython/wiki/CythonExtensionsOnWindows
.. [changelog] https://docs.python.org/3/whatsnew/3.8.html#changes-in-the-python-api
.. [os.add_dll_directory] https://docs.python.org/3.8/library/os.html#os.add_dll_directory
