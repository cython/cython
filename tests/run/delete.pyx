"""
>>> a = A()
>>> a.f()
[2, 1]
>>> a.g()
(False, True)
>>> del_item({1: 'a', 2: 'b'}, 1)
{2: 'b'}
>>> del_item(range(10), 2)
[0, 1, 3, 4, 5, 6, 7, 8, 9]
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

def del_item(L, o):
    del L[o]
    return L
