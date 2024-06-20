# -*- coding: utf-8 -*-
# cython: language_level = 3
# mode: compile
# tag: pep3131

# compile only test since there's no way to get
# it to import another test module at runtime

# this test looks at [c]importing unicode stuff
from unicode_identifiers cimport Fα1, Γναμε2
cimport unicode_identifiers
from unicode_identifiers cimport Γναμε2 as Γναμε3

from unicode_identifiers import NormalClassΓΓ
from unicode_identifiers import NormalClassΓΓ as NörmalCläss


cdef class C(unicode_identifiers.Γναμε2):
    pass

cdef class D(Γναμε2):
    pass

cdef class E(Γναμε3):
    pass

def f():
    Fα1()
    unicode_identifiers.Fα1()


