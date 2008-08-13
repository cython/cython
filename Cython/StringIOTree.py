from cStringIO import StringIO

class StringIOTree(object):
    """
    See module docs.
    """

    def __init__(self, stream=None):
        self.prepended_children = []
        self.stream = stream # if set to None, it will be constructed on first write

    def getvalue(self):
        return ("".join([x.getvalue() for x in self.prepended_children]) +
                self.stream.getvalue())

    def copyto(self, target):
        """Potentially cheaper than getvalue as no string concatenation
        needs to happen."""
        for child in self.prepended_children:
            child.copyto(target)
        if self.stream:
            target.write(self.stream.getvalue())

    def write(self, what):
        if not self.stream:
            self.stream = StringIO()
        self.stream.write(what)

    def commit(self):
        # Save what we have written until now so that the buffer
        # itself is empty -- this makes it ready for insertion
        if self.stream:
            self.prepended_children.append(StringIOTree(self.stream))
            self.stream = None

    def insert(self, iotree):
        """
        Insert a StringIOTree (and all of its contents) at this location.
        Further writing to self appears after what is inserted.
        """
        self.commit()
        self.prepended_children.append(iotree)

    def insertion_point(self):
        """
        Returns a new StringIOTree, which is left behind at the current position
        (it what is written to the result will appear right before whatever is
        next written to self).

        Calling getvalue() or copyto() on the result will only return the
        contents written to it.
        """
        # Save what we have written until now
        # This is so that getvalue on the result doesn't include it.
        self.commit()
        # Construct the new forked object to return
        other = StringIOTree()
        self.prepended_children.append(other)
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
>>> a.getvalue().split()
['first', 'second', 'third']

>>> c = b.insertion_point()
>>> d = c.insertion_point()
>>> d.write('alpha\n')
>>> b.write('gamma\n')
>>> c.write('beta\n')
>>> b.getvalue().split()
['second', 'alpha', 'beta', 'gamma']
>>> i = StringIOTree()
>>> d.insert(i)
>>> i.write('inserted\n')
>>> out = StringIO()
>>> a.copyto(out)
>>> out.getvalue().split()
['first', 'second', 'alpha', 'inserted', 'beta', 'gamma', 'third']
"""