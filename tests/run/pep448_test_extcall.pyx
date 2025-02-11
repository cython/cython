# mode: run
# tag: pep448

from __future__ import print_function

__doc__ = """
>>> def f(*, w): pass
>>> try: errors_call_no_args(f)
... except TypeError: pass
... else: print("FAILED!")

>>> def f(*, a, b, c, d, e): pass
>>> try: errors_call_no_args(f)
... except TypeError: pass
... else: print("FAILED!")

>>> def f(*, kw, b): pass
>>> try: errors_call_3args_2kwargs(f)
... except TypeError: pass
... else: print("FAILED!")

>>> def f(a, b=2, *, kw): pass
>>> try: errors_call_3args_1kwarg(f)
... except TypeError: pass
... else: print("FAILED!")

>>> def f(*, kw): pass
>>> try: errors_call_1arg_1kwarg(f)
... except TypeError: pass
... else: print("FAILED!")
"""

# test for method/function calls. adapted from CPython's "test_extcall.py".

def sortdict(d):
    return '{%s}' % ', '.join(['%r: %r' % item for item in sorted(d.items())])

# We're going the use these types for extra testing

try:
    from collections import UserList, UserDict
except ImportError:
    from UserList import UserList
    from UserDict import UserDict


# We're defining four helper functions

def e(a,b):
    print(a, b)

def f(*a, **k):
    print(a, sortdict(k))

def g(x, *y, **z):
    print(x, y, sortdict(z))

def h(j=1, a=2, h=3):
    print(j, a, h)


# Argument list examples

def call_f_positional():
    """
    >>> call_f_positional()
    () {}
    (1,) {}
    (1, 2) {}
    (1, 2, 3) {}
    (1, 2, 3, 4, 5) {}
    (1, 2, 3, 4, 5) {}
    (1, 2, 3, 4, 5) {}
    (1, 2, 3, 4, 5) {}
    (1, 2, 3, 4, 5, 6, 7) {}
    (1, 2, 3, 4, 5, 6, 7) {}
    (1, 2, 3, 4, 5, 6, 7) {}
    (1, 2) {}
    """
    f()
    f(1)
    f(1, 2)
    f(1, 2, 3)
    f(1, 2, 3, *(4, 5))
    f(1, 2, 3, *[4, 5])
    f(*[1, 2, 3], 4, 5)
    f(1, 2, 3, *UserList([4, 5]))
    f(1, 2, 3, *[4, 5], *[6, 7])
    f(1, *[2, 3], 4, *[5, 6], 7)
    f(*UserList([1, 2]), *UserList([3, 4]), 5, *UserList([6, 7]))
    f(1, *[] or () and {}, *() and [], *{} or [] and (), *{} and [] or (), 2)


# Here we add keyword arguments

def call_f_kwargs():
    """
    >>> call_f_kwargs()
    (1, 2, 3) {'a': 4, 'b': 5}
    (1, 2, 3, 4, 5) {'a': 6, 'b': 7}
    (1, 2, 3, 6, 7) {'a': 8, 'b': 9, 'x': 4, 'y': 5}
    (1, 2, 3, 4, 5) {'a': 6, 'b': 7, 'c': 8}
    (1, 2, 3, 4, 5) {'a': 8, 'b': 9, 'x': 6, 'y': 7}
    (1, 2, 3) {'a': 4, 'b': 5}
    (1, 2, 3, 4, 5) {'a': 6, 'b': 7}
    (1, 2, 3, 6, 7) {'a': 8, 'b': 9, 'x': 4, 'y': 5}
    (1, 2, 3, 4, 5) {'a': 8, 'b': 9, 'x': 6, 'y': 7}
    (1, 2) {'a': 3}
    """

    f(1, 2, 3, **{'a':4, 'b':5})
    f(1, 2, 3, *[4, 5], **{'a':6, 'b':7})
    f(1, 2, 3, x=4, y=5, *(6, 7), **{'a':8, 'b': 9})
    f(1, 2, 3, *[4, 5], **{'c': 8}, **{'a':6, 'b':7})
    f(1, 2, 3, *(4, 5), x=6, y=7, **{'a':8, 'b': 9})

    f(1, 2, 3, **UserDict(a=4, b=5))
    f(1, 2, 3, *(4, 5), **UserDict(a=6, b=7))
    f(1, 2, 3, x=4, y=5, *(6, 7), **UserDict(a=8, b=9))
    f(1, 2, 3, *(4, 5), x=6, y=7, **UserDict(a=8, b=9))

    f(1, *[] or () and {}, *() and [], *{} or [] and (), *{} and [] or (), 2,
      **{} and {} or {}, **{} or {} and {}, **{} and {}, a=3)


# Examples with invalid arguments (TypeErrors). We're also testing the function
# names in the exception messages.
#
# Verify clearing of SF bug #733667

def errors_f1():
    """
    >>> errors_f1()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...got multiple values for keyword argument 'a'
    """
    f(1, 2, **{'a': -1, 'b': 5}, **{'a': 4, 'c': 6})


def errors_f2():
    """
    >>> errors_f2()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...multiple values for keyword argument 'a'
    """
    f(1, 2, **{'a': -1, 'b': 5}, a=4, c=6)


def errors_e1():
    """
    >>> try: errors_e1()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    e(c=4)


def errors_e2():
    """
    >>> try: errors_e2()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    e(a=1, b=2, c=4)


def errors_g1():
    """
    >>> errors_g1()
    Traceback (most recent call last):
      ...
    TypeError: g() takes at least 1 positional argument (0 given)

    # TypeError: g() missing 1 required positional argument: 'x'
    """
    g()


def errors_g2():
    """
    >>> errors_g2()
    Traceback (most recent call last):
      ...
    TypeError: g() takes at least 1 positional argument (0 given)

    # TypeError: g() missing 1 required positional argument: 'x'
    """
    g(*())


def errors_g3():
    """
    >>> errors_g3()
    Traceback (most recent call last):
      ...
    TypeError: g() takes at least 1 positional argument (0 given)

    # TypeError: g() missing 1 required positional argument: 'x'
    """
    g(*(), **{})


def call_g_positional():
    """
    >>> call_g_positional()
    1 () {}
    1 (2,) {}
    1 (2, 3) {}
    1 (2, 3, 4, 5) {}
    """
    g(1)
    g(1, 2)
    g(1, 2, 3)
    g(1, 2, 3, *(4, 5))



def call_nonseq_positional1():
    """
    >>> call_nonseq_positional1()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...Nothing...

    # TypeError: g() argument after * must be a sequence, not Nothing
    """
    class Nothing(object): pass
    g(*Nothing())


def call_nonseq_positional2():
    """
    >>> call_nonseq_positional2()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...Nothing...

    # TypeError: g() argument after * must be a sequence, not Nothing
    """
    class Nothing(object):
        def __len__(self): return 5
    g(*Nothing())


def call_seqlike_positional1():
    """
    >>> call_seqlike_positional1()
    0 (1, 2) {}
    """
    class Nothing(object):
        def __len__(self): return 5
        def __getitem__(self, i):
            if i<3: return i
            else: raise IndexError(i)

    g(*Nothing())


def call_seqlike_positional2():
    """
    >>> call_seqlike_positional2()
    0 (1, 2, 3) {}
    """
    class Nothing:
        def __init__(self): self.c = 0
        def __iter__(self): return self
        def __next__(self):
            if self.c == 4:
                raise StopIteration
            c = self.c
            self.c += 1
            return c
        next = __next__

    g(*Nothing())


# Make sure that the function doesn't stomp the dictionary

def call_kwargs_unmodified1():
    """
    >>> call_kwargs_unmodified1()
    1 () {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    True
    """
    d = {'a': 1, 'b': 2, 'c': 3}
    d2 = d.copy()
    g(1, d=4, **d)
    return d == d2


# What about willful misconduct?

def call_kwargs_unmodified2():
    """
    >>> call_kwargs_unmodified2()
    {}
    """
    def saboteur(**kw):
        kw['x'] = 'm'
        return kw

    d = {}
    kw = saboteur(a=1, **d)
    return d


def errors_args_kwargs_overlap():
    """
    >>> errors_args_kwargs_overlap()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...got multiple values for... argument 'x'
    """
    g(1, 2, 3, **{'x': 4, 'y': 5})


def errors_non_string_kwarg():
    """
    >>> errors_non_string_kwarg()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...keywords must be strings...
    """
    f(**{1:2})


def errors_unexpected_kwarg():
    """
    >>> errors_unexpected_kwarg()
    Traceback (most recent call last):
      ...
    TypeError: h() got an unexpected keyword argument 'e'
    """
    h(**{'e': 2})


def errors_call_nonseq():
    """
    >>> try: errors_call_nonseq()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    h(*h)


def errors_call_builtin_nonseq():
    """
    >>> try: errors_call_builtin_nonseq()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    dir(*h)


def errors_call_none_nonseq():
    """
    >>> try: errors_call_none_nonseq()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    None(*h)


def errors_call_nonmapping_kwargs():
    """
    >>> try: errors_call_nonmapping_kwargs()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    h(**h)


def errors_call_builtin_nonmapping_kwargs():
    """
    >>> try: errors_call_builtin_nonmapping_kwargs()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    dir(**h)


def errors_call_none_nonmapping_kwargs():
    """
    >>> try: errors_call_none_nonmapping_kwargs()
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    None(**h)


'''  # compile time error in Cython
def errors_call_builtin_duplicate_kwarg():
    """
    >>> errors_call_builtin_duplicate_kwarg()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...got multiple values for keyword argument 'b'
    """
    dir(b=1, **{'b': 1})
'''


# Another helper function

def f2(*a, **b):
    return a, b


def call_many_kwargs():
    """
    call_many_kwargs()
    (3, 512, True)
    """
    d = {}
    for i in range(512):
        key = 'k%d' % i
        d[key] = i
    a, b = f2(1, *(2,3), **d)
    return len(a), len(b), b == d


def call_method(Foo):
    """
    >>> class Foo(object):
    ...     def method(self, arg1, arg2):
    ...         print(arg1+arg2)

    >>> call_method(Foo)
    3
    3
    5
    5
    """
    x = Foo()
    Foo.method(*(x, 1, 2))
    Foo.method(x, *(1, 2))
    Foo.method(*(1, 2, 3))
    Foo.method(1, *[2, 3])


# A PyCFunction that takes only positional parameters should allow an
# empty keyword dictionary to pass without a complaint, but raise a
# TypeError if the dictionary is not empty

def call_builtin_empty_dict():
    """
    >>> call_builtin_empty_dict()
    """
    silence = id(1, *{})
    silence = id(1, **{})


def call_builtin_nonempty_dict():
    """
    >>> call_builtin_nonempty_dict() # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: id() ... keyword argument...
    """
    return id(1, **{'foo': 1})


''' Cython: currently just passes empty kwargs into f() while CPython keeps the content

# A corner case of keyword dictionary items being deleted during
# the function call setup. See <https://bugs.python.org/issue2016>.

def call_kwargs_modified_while_building():
    """
    >>> call_kwargs_modified_while_building()
    1 2
    """
    class Name(str):
        def __eq__(self, other):
            try:
                 del x[self]
            except KeyError:
                 pass
            return str.__eq__(self, other)
        def __hash__(self):
            return str.__hash__(self)

    x = {Name("a"):1, Name("b"):2}
    def f(a, b):
        print(a,b)
    f(**x)
'''


# Too many arguments:

def errors_call_one_arg(f):
    """
    >>> def f(): pass
    >>> try: errors_call_one_arg(f)
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    f(1)

def errors_call_2args(f):
    """
    >>> def f(a): pass
    >>> try: errors_call_2args(f)
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    f(1, 2)

def errors_call_3args(f):
    """
    >>> def f(a, b=1): pass
    >>> try: errors_call_3args(f)
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    f(1, 2, 3)


def errors_call_1arg_1kwarg(f):
    # Py3 only
    f(1, kw=3)


def errors_call_3args_2kwargs(f):
    # Py3 only
    f(1, 2, 3, b=3, kw=3)


def errors_call_3args_1kwarg(f):
    # Py3 only
    f(2, 3, 4, kw=4)


# Too few and missing arguments:

def errors_call_no_args(f):
    """
    >>> def f(a): pass
    >>> try: errors_call_no_args(f)
    ... except TypeError: pass
    ... else: print("FAILED!")

    >>> def f(a, b): pass
    >>> try: errors_call_no_args(f)
    ... except TypeError: pass
    ... else: print("FAILED!")

    >>> def f(a, b, c): pass
    >>> try: errors_call_no_args(f)
    ... except TypeError: pass
    ... else: print("FAILED!")

    >>> def f(a, b, c, d, e): pass
    >>> try: errors_call_no_args(f)
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    f()


def errors_call_one_missing_kwarg(f):
    """
    >>> def f(a, b=4, c=5, d=5): pass
    >>> try: errors_call_one_missing_kwarg(f)
    ... except TypeError: pass
    ... else: print("FAILED!")
    """
    f(c=12, b=9)
