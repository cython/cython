 


cdef class Penguin:
    cdef object food

    def __cinit__(self, food):
        self.food = food

    def __init__(self, food):
        print("eating!")

normal_penguin = Penguin('fish')
fast_penguin = Penguin.__new__(Penguin, 'wheat')  # note: not calling __init__() !
