__doc__ = """
>>> test_append([])
None
None
got error
[1, 2]
>>> test_append(A())
appending
1
appending
2
got error
<append.A instance at ...>
>>> test_append(B())
None
None
None
[1, 2, 3, 4]
"""

class A:
    def append(self, x):
        print "appending"
        return x
        
class B(list):
    def append(self, *args):
        for arg in args:
            list.append(self, arg)

def test_append(L):
    print L.append(1)
    print L.append(2)
    try:
        print L.append(3,4)
    except TypeError:
        print "got error"
    print L

