
# tests copied from test/test_bool.py in Py2.7

cdef assertEqual(a,b):
    assert a == b, '%r != %r' % (a,b)

cdef assertIs(a,b):
    assert a is b, '%r is not %r' % (a,b)

cdef assertIsNot(a,b):
    assert a is not b, '%r is %r' % (a,b)

cdef assertNotIsInstance(a,b):
    assert not isinstance(a,b), 'isinstance(%r, %s)' % (a,b)


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

def test_repr():
    """
    >>> test_repr()
    """
    assertEqual(repr(False), 'False')
    assertEqual(repr(True), 'True')
    assertEqual(eval(repr(False)), False)
    assertEqual(eval(repr(True)), True)

def test_str():
    """
    >>> test_str()
    """
    assertEqual(str(False), 'False')
    assertEqual(str(True), 'True')

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
    assertEqual(~False, -1)
    assertEqual(~True, -2)

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

    y = x = [1]
    assertIs(x is y, True)
    assertIs(x is not y, False)

    assertIs(1 in x, True)
    assertIs(0 in x, False)
    assertIs(1 not in x, False)
    assertIs(0 not in x, True)

    y = x = {1: 2}
    assertIs(x is y, True)
    assertIs(x is not y, False)

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
    assertIs(bool(10), True)
    assertIs(bool(1), True)
    assertIs(bool(-1), True)
    assertIs(bool(0), False)
    assertIs(bool("hello"), True)
    assertIs(bool(""), False)
    assertIs(bool(), False)

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
