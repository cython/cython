#cython: boundscheck=False

print 3

cimport python_dict as asadf, python_exc, cython as cy

@cy.boundscheck(False)
def f(object[int, 2] buf):
    print buf[3, 2]

@cy.boundscheck(True)
def g(object[int, 2] buf):
    # Please leave this comment, 
#cython: this should have no special meaning
    # even if the above line doesn't follow indentation.
    print buf[3, 2]

def h(object[int, 2] buf):
    print buf[3, 2]
    with cy.boundscheck(True):
        print buf[3,2]
