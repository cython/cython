class Spam:

    def __init__(self, w):
        self.weight = w

    def serve(self):
        print self.weight, u"tons of spam!"

def order():
    """
    >>> order()
    42 tons of spam!
    """
    s = Spam(42)
    s.serve()
