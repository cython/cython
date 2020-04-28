# mode: error
# tag: assert

def nontrivial_assert_in_nogil(int a, obj):
    with nogil:
        # NOK
        assert obj
        assert a*obj
        assert a, f"123{a}xyz"

        # OK
        assert a
        assert a*a
        assert a, "abc"
        assert a, u"abc"


_ERRORS = """
7:15: Truth-testing Python object not allowed without gil
8:15: Converting to Python object not allowed without gil
8:16: Operation not allowed without gil
8:16: Truth-testing Python object not allowed without gil
9:18: String concatenation not allowed without gil
9:18: String formatting not allowed without gil
"""
