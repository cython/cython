# mode: error
# tag: pep448

def unpack_mix_in_set():
    {*1, **2}


_ERRORS = """
5:9: unexpected **item found in set literal
"""
