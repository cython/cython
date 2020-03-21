import cython

_inline_divcode = '''\
def f(int a, int b):
    return a/b
return f'''

def inline_langversion(language_level, a=5, b=2):
    """
    >>> inline_langversion(2)
    2
    >>> inline_langversion(3)
    2.5
    """
    # Caching for inline code didn't always respect language version.
    # https://github.com/cython/cython/issues/3419
    print(cython.inline(_inline_divcode, language_level=language_level, quiet=True)(a=a, b=b))
