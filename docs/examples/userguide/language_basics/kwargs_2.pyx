def g(a, b, *, c, d):
    # ...
    return 'hello world'

# We cannot call g with less verbosity than this.
foo = g(4.0, "something", c=68, d="other")
