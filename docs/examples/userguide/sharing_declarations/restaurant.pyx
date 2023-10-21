cimport dishes
from dishes cimport SpamDish

cdef void prepare(SpamDish *d):
    d.oz_of_spam = 42
    d.filler = dishes.Sausage

def serve():
    cdef SpamDish d
    prepare(&d)
    print(f'{d.oz_of_spam} oz spam, filler no. {d.filler}')
