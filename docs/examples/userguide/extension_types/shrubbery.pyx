from __future__ import print_function

cdef class Shrubbery:
    cdef int width, height

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def describe(self):
        print("This shrubbery is", self.width,
              "by", self.height, "cubits.")
