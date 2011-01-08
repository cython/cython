cdef class CheeseShop:
    cdef object cheeses

    def __cinit__(self):
        self.cheeses = []

    property cheese:

        "A senseless waste of a property."

        def __get__(self):
            return "We don't have: %s" % self.cheeses

        def __set__(self, value):
            self.cheeses.append(value)

        def __del__(self):
            del self.cheeses[:]
