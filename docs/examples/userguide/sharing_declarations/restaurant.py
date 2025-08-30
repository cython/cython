import cython
from cython.cimports.dishes import spamdish, sausage

@cython.cfunc
def prepare(d: cython.pointer[spamdish]) -> cython.void:
    d.oz_of_spam = 42
    d.filler = sausage

def serve():
    d: spamdish
    prepare(cython.address(d))
    print(f'{d.oz_of_spam} oz spam, filler no. {d.filler}')
