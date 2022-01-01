# mode: run
# tag: cpp

cdef:
    struct S1:
        int i

    struct S2:
        int i

    extern from *:
        """
        class testclass {
        public:
            int a() {
                return 9000;
            }
            int a(unsigned int i) {
                return i;
            }
        };
        """

        cppclass testclass:
            testclass()
            int a()
            int a(unsigned int i)

    cppclass testclass2(testclass):
        testclass2()

    cppclass testclass3(testclass):
        testclass3()
        void a(S1 v)

    cppclass testclass4(testclass):
        testclass4()
        void a(S2 v)

def test_base_class_functions(arg=None):
    """
    >>> test_base_class_functions()
    9000
    >>> test_base_class_functions(1)
    1
    """
    return testclass().a(arg) if arg else testclass().a()

def test_testclass2_functions(arg=None):
    """
    >>> test_testclass2_functions()
    9000
    >>> test_testclass2_functions(2)
    2
    """
    return testclass2().a(arg) if arg else testclass2().a()

def test_testclass3_functions(s):
    """
    >>> test_testclass3_functions()
    9000
    >>> test_testclass3_functions(3)
    3
    >>> test_testclass3_functions('s1')

    """
    cdef S1 s1
    if type(s) == 'int':
        return testclass3().a(3)
    elif s == 's1':
        return testclass3().a(s1)
    return testclass3().a()

def test_testclass4_functions(s):
    """
    >>> test_testclass4_functions()
    9000
    >>> test_testclass4_functions(4)
    4
    >>> test_testclass4_functions('s2')

    """
    cdef S2 s2
    if type(s) == 'int':
        return testclass4().a(4)
    elif s == 's2':
        return testclass4().a(s2)
    return testclass4().a()
