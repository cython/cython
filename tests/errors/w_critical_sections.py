# mode: compile
# tag: warnings

import cython

class PyC:
    @cython.critical_section
    def func(self):
        return self.a

@cython.cclass
class ExtC:
    a: cython.int

    @cython.critical_section  # no warning, good
    def func(self):
        a = self.a  # OK
        b = self.b  # Not OK
        self.b = a  # Not OK
        self.a = b  # OK

def function(o1: ExtC, o2):
    with cython.critical_section(o1, o2):
        x = o1.a  # OK
        y = o1.b  # Not OK
        o2.a = x  # not OK
    return y


_WARNINGS = """
7:4: @critical_section on method of a class that is not an extension type is unlikely to be useful
9:19: Python attribute access is not usefully protected by critical_section
18:16: Python attribute access is not usefully protected by critical_section
19:12: Python attribute access is not usefully protected by critical_section
25:14: Python attribute access is not usefully protected by critical_section
26:10: Python attribute access is not usefully protected by critical_section
"""
