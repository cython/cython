cdef class Spam:
    cdef pub i32 tons
    cdef readonly f32 tastiness
    cdef i32 temperature

    def __init__(self, tons, tastiness, temperature):
        self.tons = tons
        self.tastiness = tastiness
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature
