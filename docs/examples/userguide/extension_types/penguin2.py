import cython

@cython.freelist(8)
@cython.cclass
class Penguin:
    food: object
    def __cinit__(self, food):
        self.food = food

penguin = Penguin('fish 1')
penguin = None
penguin = Penguin('fish 2')  # does not need to allocate memory!
