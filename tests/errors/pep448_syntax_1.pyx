# mode: error
# tag: pep448

def unpack_mix():
    [*1, **1]


_ERRORS = """
5:9: Expected an identifier or literal
"""
