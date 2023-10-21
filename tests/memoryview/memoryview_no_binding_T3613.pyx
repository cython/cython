# mode: compile
# tag: memoryview

# cython: binding=false

# See GH 3613 - when memoryviews were compiled with binding off they ended up in an
# inconsistent state where different directives were applied at different stages
# of the pipeline

import cython

def f(f64[:] a):
    pass

@cython.binding(false)
def g(f64[:] a):
    pass

@cython.binding(true)
def h(f64[:] a):
    pass
