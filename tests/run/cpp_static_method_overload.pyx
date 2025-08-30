# mode: run
# tag: cpp, no-cpp-locals

cdef extern from *:
    """
    struct Foo
    {

      static const char* bar(int x, int y) {
        return "second";
      }

      static const char* bar(int x) {
        return "first";
      }

      const char* baz(int x, int y) {
        return "second";
      }

      const char* baz(int x) {
        return "first";
      }
    };
    """
    cppclass Foo:
        @staticmethod
        const char* bar(int x)

        @staticmethod
        const char* bar(int x, int y)

        const char* baz(int x)
        const char* baz(int x, int y)

def test_normal_method_overload():
    """
    >>> test_normal_method_overload()
    """
    cdef Foo f
    assert f.baz(1) == b"first"
    assert f.baz(1, 2) == b"second"

def test_static_method_overload():
    """
    >>> test_static_method_overload()
    """
    assert Foo.bar(1) == b"first"
    assert Foo.bar(1, 2) == b"second"
