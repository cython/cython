"""
>>> a = A()
>>> a.f()
[2, 1]
>>> a.g()
(False, True)
"""

class A:
    def f(self):
        self.refs = [3,2,1]
        del self.refs[0]
        return self.refs

    def g(self):
        self.a = 3
        del self.a
        return (hasattr(self, u"a"), hasattr(self, u"g"))
