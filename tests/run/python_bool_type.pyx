# tests copied from test/test_bool.py in Py3.14

from contextlib import contextmanager


cdef assertEqual(a,b):
    assert a == b, '%r != %r' % (a,b)

cdef assertGreaterEqual(a,b):
    assert a >= b, '%r < %r' % (a,b)

cdef assertIs(a,b):
    assert a is b, '%r is not %r' % (a,b)

cdef assertIsNot(a,b):
    assert a is not b, '%r is %r' % (a,b)

cdef assertNotIsInstance(a,b):
    assert not isinstance(a,b), 'isinstance(%r, %s)' % (a,b)

def assertRaises(exc_type, func=None, *args):
    if func is not None:
        try:
            func(*args)
        except exc_type as exc:
            pass
        else:
            assert False, f"Exception {exc_type} was not raised"
    else:
        @contextmanager
        def cm(exc_type):
            try:
                yield
            except exc_type as exc:
                pass
            else:
                assert False, f"Exception {exc_type} was not raised"

        return cm(exc_type)

@contextmanager
def assertRaisesRegex(exc_type, regex):
    try:
        yield
    except exc_type as exc:
        # Ignore regex
        pass
    else:
        assert False, f"Exception {exc_type} was not raised"


def test_repr():
    """
    >>> test_repr()
    """
    assertEqual(repr(False), 'False')
    assertEqual(repr(True), 'True')
    assertIs(eval(repr(False)), False)
    assertIs(eval(repr(True)), True)


def test_str():
    """
    >>> test_str()
    """
    assertEqual(str(False), 'False')
    assertEqual(str(True), 'True')


def test_int():
    """
    >>> test_int()
    """
    assertEqual(int(False), 0)
    assertIsNot(int(False), False)
    assertEqual(int(True), 1)
    assertIsNot(int(True), True)


def test_float():
    """
    >>> test_float()
    """
    assertEqual(float(False), 0.0)
    assertIsNot(float(False), False)
    assertEqual(float(True), 1.0)
    assertIsNot(float(True), True)


def test_complex():
    """
    >>> test_complex()
    """
    assertEqual(complex(False), 0j)
    assertEqual(complex(False), False)
    assertEqual(complex(True), 1+0j)
    assertEqual(complex(True), True)


def test_math():
    """
    >>> test_math()
    """
    assertEqual(+False, 0)
    assertIsNot(+False, False)
    assertEqual(-False, 0)
    assertIsNot(-False, False)
    assertEqual(abs(False), 0)
    assertIsNot(abs(False), False)
    assertEqual(+True, 1)
    assertIsNot(+True, True)
    assertEqual(-True, -1)
    assertEqual(abs(True), 1)
    assertIsNot(abs(True), True)

    '''
    with assertWarns(DeprecationWarning):
        # We need to put the bool in a variable, because the constant
        # ~False is evaluated at compile time due to constant folding;
        # consequently the DeprecationWarning would be issued during
        # module loading and not during test execution.
        false = False
        assertEqual(~false, -1)
    with assertWarns(DeprecationWarning):
        # also check that the warning is issued in case of constant
        # folding at compile time
        assertEqual(eval("~False"), -1)
    with assertWarns(DeprecationWarning):
        true = True
        assertEqual(~true, -2)
    with assertWarns(DeprecationWarning):
        assertEqual(eval("~True"), -2)
    '''

    assertEqual(False+2, 2)
    assertEqual(True+2, 3)
    assertEqual(2+False, 2)
    assertEqual(2+True, 3)

    assertEqual(False+False, 0)
    assertIsNot(False+False, False)
    assertEqual(False+True, 1)
    assertIsNot(False+True, True)
    assertEqual(True+False, 1)
    assertIsNot(True+False, True)
    assertEqual(True+True, 2)

    assertEqual(True-True, 0)
    assertIsNot(True-True, False)
    assertEqual(False-False, 0)
    assertIsNot(False-False, False)
    assertEqual(True-False, 1)
    assertIsNot(True-False, True)
    assertEqual(False-True, -1)

    assertEqual(True*1, 1)
    assertEqual(False*1, 0)
    assertIsNot(False*1, False)

    assertEqual(True/1, 1)
    assertIsNot(True/1, True)
    assertEqual(False/1, 0)
    assertIsNot(False/1, False)

    assertEqual(True%1, 0)
    assertIsNot(True%1, False)
    assertEqual(True%2, 1)
    assertIsNot(True%2, True)
    assertEqual(False%1, 0)
    assertIsNot(False%1, False)

    for b in False, True:
        for i in 0, 1, 2:
            assertEqual(b**i, int(b)**i)
            assertIsNot(b**i, bool(int(b)**i))

    for a in False, True:
        for b in False, True:
            assertIs(a&b, bool(int(a)&int(b)))
            assertIs(a|b, bool(int(a)|int(b)))
            assertIs(a^b, bool(int(a)^int(b)))
            assertEqual(a&int(b), int(a)&int(b))
            assertIsNot(a&int(b), bool(int(a)&int(b)))
            assertEqual(a|int(b), int(a)|int(b))
            assertIsNot(a|int(b), bool(int(a)|int(b)))
            assertEqual(a^int(b), int(a)^int(b))
            assertIsNot(a^int(b), bool(int(a)^int(b)))
            assertEqual(int(a)&b, int(a)&int(b))
            assertIsNot(int(a)&b, bool(int(a)&int(b)))
            assertEqual(int(a)|b, int(a)|int(b))
            assertIsNot(int(a)|b, bool(int(a)|int(b)))
            assertEqual(int(a)^b, int(a)^int(b))
            assertIsNot(int(a)^b, bool(int(a)^int(b)))

    assertIs(1==1, True)
    assertIs(1==0, False)
    assertIs(0<1, True)
    assertIs(1<0, False)
    assertIs(0<=0, True)
    assertIs(1<=0, False)
    assertIs(1>0, True)
    assertIs(1>1, False)
    assertIs(1>=1, True)
    assertIs(0>=1, False)
    assertIs(0!=1, True)
    assertIs(0!=0, False)

    x = [1]
    assertIs(x is x, True)
    assertIs(x is not x, False)

    assertIs(1 in x, True)
    assertIs(0 in x, False)
    assertIs(1 not in x, False)
    assertIs(0 not in x, True)

    x = {1: 2}
    assertIs(x is x, True)
    assertIs(x is not x, False)

    assertIs(1 in x, True)
    assertIs(0 in x, False)
    assertIs(1 not in x, False)
    assertIs(0 not in x, True)

    assertIs(not True, False)
    assertIs(not False, True)


def test_convert():
    """
    >>> test_convert()
    """
    assertRaises(TypeError, bool, 42, 42)
    assertIs(bool(10), True)
    assertIs(bool(1), True)
    assertIs(bool(-1), True)
    assertIs(bool(0), False)
    assertIs(bool("hello"), True)
    assertIs(bool(""), False)
    assertIs(bool(), False)


def test_keyword_args():
    """
    >>> test_keyword_args()
    """
    with assertRaisesRegex(TypeError, 'keyword argument'):
        bool(x=10)


def test_format():
    """
    >>> test_format()
    """
    assertEqual("%d" % False, "0")
    assertEqual("%d" % True, "1")
    assertEqual("%x" % False, "0")
    assertEqual("%x" % True, "1")


def test_hasattr():
    """
    >>> test_hasattr()
    """
    assertIs(hasattr([], "append"), True)
    assertIs(hasattr([], "wobble"), False)


def test_callable():
    """
    >>> test_callable()
    """
    assertIs(callable(len), True)
    assertIs(callable(1), False)


def test_isinstance():
    """
    >>> test_isinstance()
    """
    assertIs(isinstance(True, bool), True)
    assertIs(isinstance(False, bool), True)
    assertIs(isinstance(True, int), True)
    assertIs(isinstance(False, int), True)
    assertIs(isinstance(1, bool), False)
    assertIs(isinstance(0, bool), False)


def test_issubclass():
    """
    >>> test_issubclass()
    """
    assertIs(issubclass(bool, int), True)
    assertIs(issubclass(int, bool), False)


def test_contains():
    """
    >>> test_contains()
    """
    assertIs(1 in {}, False)
    assertIs(1 in {1:1}, True)


def test_string():
    """
    >>> test_string()
    """
    assertIs("xyz".endswith("z"), True)
    assertIs("xyz".endswith("x"), False)
    assertIs("xyz0123".isalnum(), True)
    assertIs("@#$%".isalnum(), False)
    assertIs("xyz".isalpha(), True)
    assertIs("@#$%".isalpha(), False)
    assertIs("0123".isdigit(), True)
    assertIs("xyz".isdigit(), False)
    assertIs("xyz".islower(), True)
    assertIs("XYZ".islower(), False)
    assertIs("0123".isdecimal(), True)
    assertIs("xyz".isdecimal(), False)
    assertIs("0123".isnumeric(), True)
    assertIs("xyz".isnumeric(), False)
    assertIs(" ".isspace(), True)
    assertIs("\xa0".isspace(), True)
    assertIs("\u3000".isspace(), True)
    assertIs("XYZ".isspace(), False)
    assertIs("X".istitle(), True)
    assertIs("x".istitle(), False)
    assertIs("XYZ".isupper(), True)
    assertIs("xyz".isupper(), False)
    assertIs("xyz".startswith("x"), True)
    assertIs("xyz".startswith("z"), False)


def test_boolean():
    """
    >>> test_boolean()
    """
    assertEqual(True & 1, 1)
    assertNotIsInstance(True & 1, bool)
    assertIs(True & True, True)

    assertEqual(True | 1, 1)
    assertNotIsInstance(True | 1, bool)
    assertIs(True | True, True)

    assertEqual(True ^ 1, 0)
    assertNotIsInstance(True ^ 1, bool)
    assertIs(True ^ True, False)


'''
# Useless in Cython and requires 'os_helper'.
def test_fileclosed():
    """
    >>> test_fileclosed()
    """
    try:
        with open(os_helper.TESTFN, "w", encoding="utf-8") as f:
            assertIs(f.closed, False)
        assertIs(f.closed, True)
    finally:
        os.remove(os_helper.TESTFN)
'''


def test_types():
    """
    >>> test_types()
    """
    # types are always true.
    for t in [bool, complex, dict, float, int, list, object,
                set, str, tuple, type]:
        assertIs(bool(t), True)


def test_operator():
    """
    >>> test_operator()
    """
    import operator
    assertIs(operator.truth(0), False)
    assertIs(operator.truth(1), True)
    assertIs(operator.not_(1), False)
    assertIs(operator.not_(0), True)
    assertIs(operator.contains([], 1), False)
    assertIs(operator.contains([1], 1), True)
    assertIs(operator.lt(0, 0), False)
    assertIs(operator.lt(0, 1), True)
    assertIs(operator.is_(True, True), True)
    assertIs(operator.is_(True, False), False)
    assertIs(operator.is_not(True, True), False)
    assertIs(operator.is_not(True, False), True)


def test_marshal():
    """
    >>> test_marshal()
    """
    import marshal
    assertIs(marshal.loads(marshal.dumps(True)), True)
    assertIs(marshal.loads(marshal.dumps(False)), False)


def test_pickle():
    """
    >>> test_pickle()
    """
    import pickle
    for proto in range(pickle.HIGHEST_PROTOCOL + 1):
        assertIs(pickle.loads(pickle.dumps(True, proto)), True)
        assertIs(pickle.loads(pickle.dumps(False, proto)), False)


def test_picklevalues():
    """
    >>> test_picklevalues()
    """
    # Test for specific backwards-compatible pickle values
    import pickle
    assertEqual(pickle.dumps(True, protocol=0), b"I01\n.")
    assertEqual(pickle.dumps(False, protocol=0), b"I00\n.")
    assertEqual(pickle.dumps(True, protocol=1), b"I01\n.")
    assertEqual(pickle.dumps(False, protocol=1), b"I00\n.")
    assertEqual(pickle.dumps(True, protocol=2), b'\x80\x02\x88.')
    assertEqual(pickle.dumps(False, protocol=2), b'\x80\x02\x89.')


def test_convert_to_bool():
    """
    >>> test_convert_to_bool()
    """
    # Verify that TypeError occurs when bad things are returned
    # from __bool__().  This isn't really a bool test, but
    # it's related.
    check = lambda o: assertRaises(TypeError, bool, o)
    class Foo(object):
        def __bool__(self):
            return self
    check(Foo())

    class Bar(object):
        def __bool__(self):
            return "Yes"
    check(Bar())

    class Baz(int):
        def __bool__(self):
            return self
    check(Baz())

    # __bool__() must return a bool not an int
    class Spam(int):
        def __bool__(self):
            return 1
    check(Spam())

    class Eggs:
        def __len__(self):
            return -1
    assertRaises(ValueError, bool, Eggs())


def test_interpreter_convert_to_bool_raises():
    """
    >>> test_interpreter_convert_to_bool_raises()
    """
    class SymbolicBool:
        def __bool__(self):
            raise TypeError

    class Symbol:
        def __gt__(self, other):
            return SymbolicBool()

    x = Symbol()

    with assertRaises(TypeError):
        if x > 0:
            msg = "x > 0 was true"
        else:
            msg = "x > 0 was false"

    # This used to create negative refcounts, see gh-102250
    del x


def test_from_bytes():
    """
    >>> test_from_bytes()
    """
    assertIs(bool.from_bytes(b'\x00'*8, 'big'), False)
    assertIs(bool.from_bytes(b'abcd', 'little'), True)


def test_sane_len():
    """
    >>> test_sane_len()
    """
    # this test just tests our assumptions about __len__
    # this will start failing if __len__ changes assertions
    for badval in ['illegal', -1, 1 << 32]:
        class A:
            def __len__(self):
                return badval
        try:
            bool(A())
        except (Exception) as e_bool:
            try:
                len(A())
            except (Exception) as e_len:
                assertEqual(str(e_bool), str(e_len))


def test_blocked():
    """
    >>> test_blocked()
    """
    class A:
        __bool__ = None
    assertRaises(TypeError, bool, A())

    class B:
        def __len__(self):
            return 10
        __bool__ = None
    assertRaises(TypeError, bool, B())

    class C:
        __len__ = None
    assertRaises(TypeError, bool, C())


def test_real_and_imag():
    """
    >>> test_real_and_imag()
    """
    assertEqual(True.real, 1)
    assertEqual(True.imag, 0)
    assertIs(type(True.real), int)
    assertIs(type(True.imag), int)
    assertEqual(False.real, 0)
    assertEqual(False.imag, 0)
    assertIs(type(False.real), int)
    assertIs(type(False.imag), int)


def test_bool_called_at_least_once():
    """
    >>> test_bool_called_at_least_once()
    """
    class X:
        def __init__(self):
            self.count = 0
        def __bool__(self):
            self.count += 1
            return True

    def f(x):
        if x or True:
            pass

    x = X()
    f(x)
    assertGreaterEqual(x.count, 1)


def test_bool_new():
    """
    >>> test_bool_new()
    """
    assertIs(bool.__new__(bool), False)
    assertIs(bool.__new__(bool, 1), True)
    assertIs(bool.__new__(bool, 0), False)
    assertIs(bool.__new__(bool, False), False)
    assertIs(bool.__new__(bool, True), True)
