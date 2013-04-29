# mode: error
# tag: werror

cimport cython

s = "abc"
l = [1, 2, 3]

def normal_wraparound(int i, bytes B not None, list L not None):
    a = s[:]
    a = s[1:2]
    a = s[-2:-1]
    a = "abc"[-2:-1]
    a = "abc"[-2:i]
    a = B[-2:-1]
    a = B[:-1]
    a = B[-2:]

    b = l[1:2]
    b = l[:2]
    b = l[1:]
    b = l[-2:-1]
    b = [1, 2, 3][-2:-1]
    b = [1, 2, 3][-2:i]
    b = L[-2:-1]

@cython.wraparound(False)
def no_wraparound(int i, bytes B not None, list L not None):
    a = s[:]
    a = s[1:2]
    a = s[-2:-1]
    a = "abc"[-2:-1]  # evaluated at compile time
    a = "abc"[-2:i]
    a = B[:]
    a = B[-2:-1]
    a = B[:-1]
    a = B[-2:]

    b = l[1:2]
    b = l[:2]
    b = l[1:]
    b = l[-2:-1]
    b = [1, 2, 3][-2:i]
    b = L[-2:-1]


_ERRORS = """
31:11: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
31:14: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
33:15: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
35:11: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
35:14: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
36:12: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
37:11: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
42:11: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
42:14: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
43:19: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
44:11: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
44:14: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
"""
