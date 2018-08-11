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

.. [WinInst] https://github.com/cython/cython/wiki/CythonExtensionsOnWindows
