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

    def fork(self):
        # Save what we have written until now
        # (would it be more efficient to check with len(self.stream.getvalue())?
        # leaving it out for now)
        self.prepended_children.append(StringIOTree(self.stream))
        # Construct the new forked object to return
        other = StringIOTree()
        self.prepended_children.append(other)
        self.stream = StringIO()
        return other

__doc__ = r"""
Implements a forkable buffer. When you know you need to "get back" to a place
and write more later, simply call fork() at that spot and get a new
StringIOTree object that is "left behind", *behind* the object that is
forked.

EXAMPLE:

>>> pyrex = StringIOTree()
>>> pyrex.write('first\n')
>>> cython = pyrex.fork()
>>> pyrex.write('third\n')
>>> cython.write('second\n')
>>> print pyrex.getvalue()
first
second
third
<BLANKLINE>

>>> b = cython.fork()
>>> a = b.fork()
>>> a.write('alpha\n')
>>> cython.write('gamma\n')
>>> b.write('beta\n')
>>> print cython.getvalue()
second
alpha
beta
gamma
<BLANKLINE>

>>> out = StringIO()
>>> pyrex.copyto(out)
>>> print out.getvalue()
first
second
alpha
beta
gamma
third
<BLANKLINE>
"""
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
