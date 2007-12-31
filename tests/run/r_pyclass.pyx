__doc__ = """
    >>> order()
    42 tons of spam!
"""

class Spam:

    def __init__(self, w):
        self.weight = w

    def serve(self):
        print self.weight, "tons of spam!"

def order():
    s = Spam(42)
    s.serve()
