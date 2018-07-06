def f(a, b, *args, c, d = 42, e, **kwds):
    ...


# We cannot call f with less verbosity than this.
foo = f(4, "bar", c=68, e=1.0)
