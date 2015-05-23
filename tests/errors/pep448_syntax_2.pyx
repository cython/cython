# mode: error
# tag: pep448

def unpack_wrong_stars():
    [**1]


_ERRORS = """
5:5: Expected an identifier or literal
"""
