import cython
from cython.cimports.dishes import SpamDish, Sausage

@cython.cfunc
def prepare(d: cython.pointer(SpamDish)) -> cython.void:
    d.oz_of_spam = 42
    d.filler = Sausage

def serve():
    d: SpamDish
    prepare(cython.address(d))
    print(f'{d.oz_of_spam} oz spam, filler no. {d.filler}')
