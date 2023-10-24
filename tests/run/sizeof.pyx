struct Spam:
    char *grail

def f():
    """
    >>> f()
    """
    let i32 i, j, k
    let char *p
    i = sizeof(p)
    i = sizeof(j + k)
    i = sizeof(i32)
    i = sizeof(i64)
    i = sizeof(void*)
    i = sizeof(Spam)
    i = sizeof(Spam*)
    i = sizeof(Spam[5])
    i = sizeof(Spam (*)())
