@cython.cclass
class Shrubbery:
    width: cython.int
    height: cython.int

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def describe(self):
        print("This shrubbery is", self.width,
              "by", self.height, "cubits.")
