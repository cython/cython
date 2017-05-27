#!/usr/bin/env python
# encoding: utf-8

from nose.tools import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from _cython_dependencies import CythonDependencyScanner

class _CythonTest(object):
    def setUp(self):
        self.c = CythonDependencyScanner([])


class Test_CythonDependencyTracking(_CythonTest): # {{{
    def test_simple_from(self):
        self.c._find_deps("""from blub cimport hallo""")

        ok_("blub.pxd" in self.c.deps)
        eq_(len(self.c.deps), 1)
    def test_simple_from_submodul(self):
        self.c._find_deps("""from geometry.objects cimport hi""")

        ok_("geometry/objects.pxd" in self.c.deps)
        eq_(len(self.c.deps), 1)

    def test_simple_cimport(self):
        self.c._find_deps("""cimport hallo""")

        ok_("hallo.pxd" in self.c.deps)
        eq_(len(self.c.deps), 1)

    def test_simple_cimport_from_submodule(self):
        self.c._find_deps("""cimport hallo.welt""")

        ok_("hallo/welt.pxd" in self.c.deps)
        eq_(len(self.c.deps), 1)

    def test_multiple_cimport(self):
        self.c._find_deps("""cimport hallo, sunshine""")

        ok_("hallo.pxd" in self.c.deps)
        ok_("sunshine.pxd" in self.c.deps)
        eq_(len(self.c.deps), 2)
    def test_cimport_with_as(self):
        self.c._find_deps("""cimport hallo as h""")

        ok_("hallo.pxd" in self.c.deps)
        eq_(len(self.c.deps), 1)


    def test_simple_include(self):
        self.c._find_deps('include "hello.pxi"')

        ok_("hello.pxi" in self.c.deps)
        eq_(len(self.c.deps), 1)

    def test_simple_cheader(self):
        self.c._find_deps('cdef extern from "hello.h"')

        ok_("hello.h" in self.c.deps)
        eq_(len(self.c.deps), 1)

    def test_realworld_example(self):
        self.c._find_deps('''
cdef extern from "math.h":
    double sqrt(double)

from geom cimport Triangle, Rect
cimport Integrator, House

def import_function():
    pass
''')

        ok_("math.h" in self.c.deps)
        ok_("geom.pxd" in self.c.deps)

        ok_("Integrator.pxd" in self.c.deps)
        ok_("House.pxd" in self.c.deps)

        eq_(len(self.c.deps), 4)



