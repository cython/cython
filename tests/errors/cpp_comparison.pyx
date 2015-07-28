# mode: error
# tag: cpp

from libcpp.vector cimport vector

def vector_is_none(vector[int] iv):
    # TODO: this isn't strictly wrong, so it might be allowed as a 'feature' at some point
    if iv is None:
        pass


_ERRORS = """
8:10: Invalid types for 'is' (vector[int], Python object)
"""
