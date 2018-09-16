def myfunction(x, y=2):
    a = x - y
    return a + x * y

def _helper(a):
    return a + 1

class A:
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    def foo(self, x):
        print(x + _helper(1.0))
