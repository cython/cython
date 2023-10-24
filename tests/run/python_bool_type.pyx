# tests copied from test/test_bool.py in Py2.7

fn assertEqual(a, b):
    assert a == b, '%r != %r' % (a, b)

fn assertIs(a, b):
    assert a is b, '%r is not %r' % (a, b)

fn assertIsNot(a, b):
    assert a is not b, '%r is %r' % (a, b)

fn assertNotIsInstance(a, b):
    assert not isinstance(a, b), 'isinstance(%r, %s)' % (a, b)

def test_int():
    """
    >>> test_int()
    """
    assertEqual(int(false), 0)
    assertIsNot(int(false), false)
    assertEqual(int(true), 1)
    assertIsNot(int(true), true)

def test_float():
    """
    >>> test_float()
    """
    assertEqual(float(false), 0.0)
    assertIsNot(float(false), false)
    assertEqual(float(true), 1.0)
    assertIsNot(float(true), true)

def test_repr():
    """
    >>> test_repr()
    """
    assertEqual(repr(false), 'False')
    assertEqual(repr(true), 'True')
    assertEqual(eval(repr(false)), false)
    assertEqual(eval(repr(true)), true)

def test_str():
    """
    >>> test_str()
    """
    assertEqual(str(false), 'False')
    assertEqual(str(true), 'True')

def test_math():
    """
    >>> test_math()
    """
    assertEqual(+false, 0)
    assertIsNot(+false, false)
    assertEqual(-false, 0)
    assertIsNot(-false, false)
    assertEqual(abs(false), 0)
    assertIsNot(abs(false), false)
    assertEqual(+true, 1)
    assertIsNot(+true, true)
    assertEqual(-true, -1)
    assertEqual(abs(true), 1)
    assertIsNot(abs(true), true)
    assertEqual(~false, -1)
    assertEqual(~true, -2)

    assertEqual(false+2, 2)
    assertEqual(true+2, 3)
    assertEqual(2+false, 2)
    assertEqual(2+true, 3)

    assertEqual(false+false, 0)
    assertIsNot(false+false, false)
    assertEqual(false+true, 1)
    assertIsNot(false+true, true)
    assertEqual(true+false, 1)
    assertIsNot(true+false, true)
    assertEqual(true+true, 2)

    assertEqual(true-true, 0)
    assertIsNot(true-true, false)
    assertEqual(false-false, 0)
    assertIsNot(false-false, false)
    assertEqual(true-false, 1)
    assertIsNot(true-false, true)
    assertEqual(false-true, -1)

    assertEqual(true*1, 1)
    assertEqual(false*1, 0)
    assertIsNot(false*1, false)

    assertEqual(true/1, 1)
    assertIsNot(true/1, true)
    assertEqual(false/1, 0)
    assertIsNot(false/1, false)

    for b in false, true:
        for i in 0, 1, 2:
            assertEqual(b**i, int(b)**i)
            assertIsNot(b**i, bool(int(b)**i))

    for a in false, true:
        for b in false, true:
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

    assertIs(1==1, true)
    assertIs(1==0, false)
    assertIs(0<1, true)
    assertIs(1<0, false)
    assertIs(0<=0, true)
    assertIs(1<=0, false)
    assertIs(1>0, true)
    assertIs(1>1, false)
    assertIs(1>=1, true)
    assertIs(0>=1, false)
    assertIs(0!=1, true)
    assertIs(0!=0, false)

    y = x = [1]
    assertIs(x is y, true)
    assertIs(x is not y, false)

    assertIs(1 in x, true)
    assertIs(0 in x, false)
    assertIs(1 not in x, false)
    assertIs(0 not in x, true)

    y = x = {1: 2}
    assertIs(x is y, true)
    assertIs(x is not y, false)

    assertIs(1 in x, true)
    assertIs(0 in x, false)
    assertIs(1 not in x, false)
    assertIs(0 not in x, true)

    assertIs(not true, false)
    assertIs(not false, true)

def test_convert():
    """
    >>> test_convert()
    """
    assertIs(bool(10), true)
    assertIs(bool(1), true)
    assertIs(bool(-1), true)
    assertIs(bool(0), false)
    assertIs(bool("hello"), true)
    assertIs(bool(""), false)
    assertIs(bool(), false)

def test_isinstance():
    """
    >>> test_isinstance()
    """
    assertIs(isinstance(true, bool), true)
    assertIs(isinstance(false, bool), true)
    assertIs(isinstance(true, int), true)
    assertIs(isinstance(false, int), true)
    assertIs(isinstance(1, bool), false)
    assertIs(isinstance(0, bool), false)

def test_issubclass():
    """
    >>> test_issubclass()
    """
    assertIs(issubclass(bool, int), true)
    assertIs(issubclass(int, bool), false)

def test_boolean():
    """
    >>> test_boolean()
    """
    assertEqual(true & 1, 1)
    assertNotIsInstance(true & 1, bool)
    assertIs(true & true, true)

    assertEqual(true | 1, 1)
    assertNotIsInstance(true | 1, bool)
    assertIs(true | true, true)

    assertEqual(true ^ 1, 0)
    assertNotIsInstance(true ^ 1, bool)
    assertIs(true ^ true, false)
