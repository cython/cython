#!/usr/bin/env python
"""
Create a C file for embedding one or more Cython source files.
Requires Cython 0.11.2 (or perhaps newer).

See README.rst for more details.
"""

import sys

if len(sys.argv) < 2:
    print >>sys.stderr, "USAGE: %s module [module ...]" % sys.argv[0]
    sys.exit(1)

def format_modname(name):
    if name.endswith('.pyx'):
        name = name[:-4]
    return name.replace('.','_')

modules = [format_modname(x) for x in sys.argv[1:]]

print """
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

#if PY_MAJOR_VERSION < 3
# define MODINIT(name)  init ## name
#else
# define MODINIT(name)  PyInit_ ## name
#endif
"""

for name in modules:
    print "PyMODINIT_FUNC MODINIT(%s) (void);" % name

print """
static struct _inittab inittab[] = {"""

for name in modules:
    print '    {"%(name)s", MODINIT(%(name)s)},' % {'name' : name}

print """    {NULL, NULL}
};

extern int __pyx_module_is_main_%(main)s;

#if PY_MAJOR_VERSION < 3 || (!defined(WIN32) && !defined(MS_WINDOWS))
int main(int argc, char** argv) {
#else
int wmain(int argc, wchar_t **argv) {
#endif
    int r = 0;
    PyObject *m = NULL;
    if (PyImport_ExtendInittab(inittab)) {
        fprintf(stderr, "No memory\\n");
        exit(1);
    }
    Py_SetProgramName(argv[0]);
    Py_Initialize();
    PySys_SetArgv(argc, argv);
    __pyx_module_is_main_%(main)s = 1;
    m = PyImport_ImportModule(inittab[0].name);
    if (!m) {
        r = 1;
        PyErr_Print(); /* This exits with the right code if SystemExit. */
        if (Py_FlushLine()); PyErr_Clear();
    }
    Py_XDECREF(m);
    Py_Finalize();
    return r;
}
""" % {'main' : modules[0]}
