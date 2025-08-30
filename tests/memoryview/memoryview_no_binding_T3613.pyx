# mode: compile
# tag: memoryview

# cython: binding=False

# See GH 3613 - when memoryviews were compiled with binding off they ended up in an
# inconsistent state where different directives were applied at different stages
# of the pipeline

import cython

def f(double[:] a):
    pass

@cython.binding(False)
def g(double[:] a):
    pass

@cython.binding(True)
def h(double[:] a):
    pass
