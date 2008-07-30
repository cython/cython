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

    def insertion_point(self):
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
Implements a buffer with insertion points. When you know you need to
"get back" to a place and write more later, simply call insertion_point()
at that spot and get a new StringIOTree object that is "left behind".

EXAMPLE:

>>> a = StringIOTree()
>>> a.write('first\n')
>>> b = a.insertion_point()
>>> a.write('third\n')
>>> b.write('second\n')
>>> print a.getvalue()
first
second
third
<BLANKLINE>

>>> c = b.insertion_point()
>>> d = c.insertion_point()
>>> d.write('alpha\n')
>>> b.write('gamma\n')
>>> c.write('beta\n')
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
<BLANKLINE>
"""
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
