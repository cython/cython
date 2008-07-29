from cStringIO import StringIO

class StringIOTree(object):
    """
    See module docs.
    """

    def __init__(self, stream=None):
        self.prepended_children = []
        if stream is None: stream = StringIO()
        self.stream = stream

    def getvalue(self):
        return ("".join([x.getvalue() for x in self.prepended_children]) +
                self.stream.getvalue())

    def copyto(self, target):
        """Potentially cheaper than getvalue as no string concatenation
        needs to happen."""
        for child in self.prepended_children:
            child.copyto(target)
        target.write(self.stream.getvalue())

    def write(self, what):
        self.stream.write(what)

    def fork(self, count=2):
        # Shuffle around the embedded StringIO objects so that
        # references to self keep writing at the end.
        self.prepended_children.append(StringIOTree(self.stream))
        self.stream = StringIO()
        tines = [StringIOTree() for i in range(1, count)]
        self.prepended_children.extend(tines)
        tines.append(self)
        return tines

__doc__ = r"""
Implements a forkable buffer. When you know you need to "get back" to a place
and write more later, simply call fork() and get.

The last buffer returned from fork() will always be the object itself; i.e.,
if code elsewhere has references to the buffer and writes to it later it will
always end up at the end just as if the fork never happened.


EXAMPLE:

>>> a = StringIOTree()
>>> a.write('first\n')
>>> b, c = a.fork()
>>> c.write('third\n')
>>> b.write('second\n')
>>> print a.getvalue()
first
second
third
<BLANKLINE>

>>> a.write('fourth\n')
>>> print a.getvalue()
first
second
third
fourth
<BLANKLINE>

>>> d, e, f = b.fork(3)
>>> d.write('alpha\n')
>>> f.write('gamma\n')
>>> e.write('beta\n')
>>> print b.getvalue()
second
alpha
beta
gamma
<BLANKLINE>

>>> out = StringIO()
>>> a.copyto(out)
>>> print out.getvalue()
first
second
alpha
beta
gamma
third
fourth
<BLANKLINE>
"""
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
