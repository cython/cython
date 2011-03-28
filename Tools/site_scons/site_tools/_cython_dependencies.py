#!/usr/bin/env python
# encoding: utf-8

import re
import os
import operator

__all__ = ["CythonDependencyScanner"]

flatten = lambda a: reduce(operator.add, a, [])
class CythonDependencyScanner(object):
    # The regular expression were originally from the sage setup.py
    _DEP_REGS_PXD = [
        re.compile(r'^ *(?:cimport +([\w\. ,]+))', re.M),
        re.compile(r'^ *(?:from +([\w.]+) +cimport)', re.M),
    ]
    _DEP_REG_DIRECT = \
        re.compile(r'^ *(?:include *[\'"]([^\'"]+)[\'"])', re.M)
    _DEP_REG_CHEADER = \
        re.compile(r'^ *(?:cdef[ ]*extern[ ]*from *[\'"]([^\'"]+)[\'"])', re.M)

    def __init__(self, include_paths):
        self.deps = set()
        self.include_paths = include_paths

    def _find_deps(self, s):
        self._find_deps_pxd(s)
        self._find_deps_cheader(s)
        self._find_deps_direct(s)

    @staticmethod
    def _normalize_module_name(s):
        # Remove as blah at the end
        s = s.split(" as ")[0].strip()

        # Replace all dots except a path seperator
        s = s.replace('.', os.path.sep)

        return s

    def _find_deps_pxd(self, s):
        temp = flatten([m.findall(s) for m in self._DEP_REGS_PXD])
        all_matches = flatten([ [ s.strip() for s in m.split(',') ] for m in temp])

        for dep in all_matches:
            dep = self._normalize_module_name(dep)
            dep += '.pxd'
            if dep not in self.deps:
                # Recurse, if file exists. If not, the file might be global
                # (which we currently do not track) or the file
                # might not exist, which is not our problem, but cythons
                for path in self.include_paths + ['']:
                    filename = os.path.relpath(os.path.join(path, dep))
                    if os.path.exists(filename):
                        self._find_deps(open(filename,"r").read())
                    self.deps.add(filename)

    def _find_deps_direct(self, s):
        all_matches = self._DEP_REG_DIRECT.findall(s)

        for dep in all_matches:
            if dep not in self.deps:
                # Recurse, if file exists. If not, the file might be global
                # (which we currently do not track) or the file
                # might not exist, which is not our problem, but cythons
                for path in self.include_paths + ['']:
                    filename = os.path.relpath(os.path.join(path, dep))
                    if os.path.exists(filename):
                        self._find_deps(open(filename,"r").read())
                    self.deps.add(filename)

    def _find_deps_cheader(self, s):
        all_matches = self._DEP_REG_CHEADER.findall(s)

        for dep in all_matches:
            if dep not in self.deps:
                # Recurse, if file exists. If not, the file might be global
                # (which we currently do not track) or the file
                # might not exist, which is not our problem, but cythons
                # TODO: we should track the headers included by this
                # header. But currently we don't
                self.deps.add(dep)

    def __call__(self, source):
        self.deps = set()

        # We might also depend on our definition file if it exists
        pxd = os.path.splitext(source)[0] + '.pxd'
        if os.path.exists(pxd):
            self.deps.add(pxd)
            self._find_deps(open(pxd, "r").read())

        self._find_deps(open(source,"r").read())
        self.deps = [ d for d in self.deps if os.path.exists(d) ]

        return self.deps

