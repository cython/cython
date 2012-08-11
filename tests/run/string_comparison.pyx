
bstring1 = b"abcdefg"
bstring2 = b"1234567"

string1 = "abcdefg"
string2 = "1234567"

ustring1 = u"abcdefg"
ustring2 = u"1234567"

# unicode

def unicode_eq(unicode s1, unicode s2):
    """
    >>> unicode_eq(ustring1, ustring1)
    True
    >>> unicode_eq(ustring1+ustring2, ustring1+ustring2)
    True
    >>> unicode_eq(ustring1, ustring2)
    False
    """
    return s1 == s2

def unicode_neq(unicode s1, unicode s2):
    """
    >>> unicode_neq(ustring1, ustring1)
    False
    >>> unicode_neq(ustring1+ustring2, ustring1+ustring2)
    False
    >>> unicode_neq(ustring1, ustring2)
    True
    """
    return s1 != s2

def unicode_literal_eq(unicode s):
    """
    >>> unicode_literal_eq(ustring1)
    True
    >>> unicode_literal_eq((ustring1+ustring2)[:len(ustring1)])
    True
    >>> unicode_literal_eq(ustring2)
    False
    """
    return s == u"abcdefg"

def unicode_literal_neq(unicode s):
    """
    >>> unicode_literal_neq(ustring1)
    False
    >>> unicode_literal_neq((ustring1+ustring2)[:len(ustring1)])
    False
    >>> unicode_literal_neq(ustring2)
    True
    """
    return s != u"abcdefg"

def unicode_cascade(unicode s1, unicode s2):
    """
    >>> unicode_cascade(ustring1, ustring1)
    True
    >>> unicode_cascade(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> unicode_cascade(ustring1, ustring2)
    False
    """
    return s1 == s2 == u"abcdefg"

def unicode_cascade_untyped_end(unicode s1, unicode s2):
    """
    >>> unicode_cascade_untyped_end(ustring1, ustring1)
    True
    >>> unicode_cascade_untyped_end(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> unicode_cascade_untyped_end(ustring1, ustring2)
    False
    """
    return s1 == s2 == u"abcdefg" == (<object>ustring1) == ustring1

# str

def str_eq(str s1, str s2):
    """
    >>> str_eq(string1, string1)
    True
    >>> str_eq(string1+string2, string1+string2)
    True
    >>> str_eq(string1, string2)
    False
    """
    return s1 == s2

def str_neq(str s1, str s2):
    """
    >>> str_neq(string1, string1)
    False
    >>> str_neq(string1+string2, string1+string2)
    False
    >>> str_neq(string1, string2)
    True
    """
    return s1 != s2

def str_literal_eq(str s):
    """
    >>> str_literal_eq(string1)
    True
    >>> str_literal_eq((string1+string2)[:len(string1)])
    True
    >>> str_literal_eq(string2)
    False
    """
    return s == "abcdefg"

def str_literal_neq(str s):
    """
    >>> str_literal_neq(string1)
    False
    >>> str_literal_neq((string1+string2)[:len(string1)])
    False
    >>> str_literal_neq(string2)
    True
    """
    return s != "abcdefg"

def str_cascade(str s1, str s2):
    """
    >>> str_cascade(string1, string1)
    True
    >>> str_cascade(string1, (string1+string2)[:len(string1)])
    True
    >>> str_cascade(string1, string2)
    False
    """
    return s1 == s2 == "abcdefg"

def str_cascade_untyped_end(str s1, str s2):
    """
    >>> str_cascade_untyped_end(string1, string1)
    True
    >>> str_cascade_untyped_end(string1, (string1+string2)[:len(string1)])
    True
    >>> str_cascade_untyped_end(string1, string2)
    False
    """
    return s1 == s2 == "abcdefg" == (<object>string1) == string1

# bytes

def bytes_eq(bytes s1, bytes s2):
    """
    >>> bytes_eq(bstring1, bstring1)
    True
    >>> bytes_eq(bstring1+bstring2, bstring1+bstring2)
    True
    >>> bytes_eq(bstring1, bstring2)
    False
    """
    return s1 == s2

def bytes_neq(bytes s1, bytes s2):
    """
    >>> bytes_neq(bstring1, bstring1)
    False
    >>> bytes_neq(bstring1+bstring2, bstring1+bstring2)
    False
    >>> bytes_neq(bstring1, bstring2)
    True
    """
    return s1 != s2

def bytes_literal_eq(bytes s):
    """
    >>> bytes_literal_eq(bstring1)
    True
    >>> bytes_literal_eq((bstring1+bstring2)[:len(bstring1)])
    True
    >>> bytes_literal_eq(bstring2)
    False
    """
    return s == b"abcdefg"

def bytes_literal_neq(bytes s):
    """
    >>> bytes_literal_neq(bstring1)
    False
    >>> bytes_literal_neq((bstring1+bstring2)[:len(bstring1)])
    False
    >>> bytes_literal_neq(bstring2)
    True
    """
    return s != b"abcdefg"

def bytes_cascade(bytes s1, bytes s2):
    """
    >>> bytes_cascade(bstring1, bstring1)
    True
    >>> bytes_cascade(bstring1, (bstring1+bstring2)[:len(bstring1)])
    True
    >>> bytes_cascade(bstring1, bstring2)
    False
    """
    return s1 == s2 == b"abcdefg"

def bytes_cascade_untyped_end(bytes s1, bytes s2):
    """
    >>> bytes_cascade_untyped_end(bstring1, bstring1)
    True
    >>> bytes_cascade_untyped_end(bstring1, (bstring1+bstring2)[:len(bstring1)])
    True
    >>> bytes_cascade_untyped_end(bstring1, bstring2)
    False
    """
    return s1 == s2 == b"abcdefg" == (<object>bstring1) == bstring1
