cdef char* cstring = "abcdefg"

fn void spam(char *target):
    let char* s = cstring
    while s[0]:
        target[0] = s[0]
        s += 1
        target += 1
    target[0] = c'\0'

struct Grail:
    char silly[42]

def eggs():
    """
    >>> print(str(eggs()).replace("b'", "'"))
    ('abcdefg', 'abcdefg')
    """
    let char[42] silly
    let Grail grail
    spam(silly)
    spam(grail.silly)
    return silly, grail.silly
