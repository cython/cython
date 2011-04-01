# mode: compile
# cython: boundscheck  =  False
# cython: ignoreme = OK
# cython: warn.undeclared = False

# This testcase is most useful if you inspect the generated C file

print 3

cimport cython as cy

def e(object[int, ndim=2] buf):
    print buf[3, 2] # no bc

@cy.boundscheck(False)
def f(object[int, ndim=2] buf):
    print buf[3, 2] # no bc

@cy.boundscheck(True)
def g(object[int, ndim=2] buf):
    # The below line should have no meaning
# cython: boundscheck = False
    # even if the above line doesn't follow indentation.
    print buf[3, 2] # bc

def h(object[int, ndim=2] buf):
    print buf[3, 2] # no bc
    with cy.boundscheck(True):
        print buf[3,2] # bc

from cython cimport boundscheck as bc

def i(object[int] buf):
    with bc(True):
        print buf[3] # bs

from cython cimport warn as my_warn

@my_warn(undeclared=True)
def j():
    pass
