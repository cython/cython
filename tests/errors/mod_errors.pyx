# mode: error

def mod_complex():
    x = (1.1+2.0j) % 4
    return x

_ERRORS = """
4:19: mod operator not supported for type 'double complex'
"""
