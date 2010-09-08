
cimport cython

ustring_with_a = u'abcdefg'
ustring_without_a = u'bcdefg'

@cython.test_fail_if_path_exists('//SimpleCallNode')
def unicode_for_loop_ord(unicode s):
    """
    >>> unicode_for_loop_ord(ustring_with_a)
    True
    >>> unicode_for_loop_ord(ustring_without_a)
    False
    """
    for c in s:
        if ord(c) == u'a':
            return True
    return False
