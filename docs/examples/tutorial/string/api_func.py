from cython.cimports.to_unicode import _text

def api_func(s):
    text_input = _text(s)
    # ...
