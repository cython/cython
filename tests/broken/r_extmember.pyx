cdef class Spam:
    cdef public int tons
    cdef readonly float tastiness
    cdef int temperature

    def __init__(self, tons, tastiness, temperature):
        self.tons = tons
        self.tastiness = tastiness
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature
