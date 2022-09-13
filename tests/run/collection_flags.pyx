# mode: run

cimport cython
import sys

@cython.collection_type("sequence")
cdef class IsSequence:
    pass

@cython.collection_type("mapping")
cdef class IsMapping:
    pass

cdef class Neither:
    pass

@cython.collection_type("mapping")
cdef class IsMappingInheritsNeither(Neither):
    pass

@cython.collection_type("mapping")
cdef class IsMappingInheritsSequence(IsSequence):
    pass

cdef class IsMappingInheritsMapping(IsMapping):
    pass

@cython.collection_type("sequence")
cdef class IsSequenceInheritsNeither(Neither):
    pass

@cython.collection_type("sequence")
cdef class IsSequenceInheritsMapping(IsMapping):
    pass

cdef class IsSequenceInheritsSequence(IsSequence):
    pass

# On Python < 3.10 the test is simply that it compiles
# TODO - when Cython supports match-case itself then test that
if sys.version_info > (3, 10):
    ns = {}
    exec("""
def test_sequence_then_mapping(x):
    match x:
        case [*_]:
            return "S"
        case {}:
            return "M"

def test_mapping_then_sequence(x):
    match x:
        case {}:
            return "M"
        case [*_]:
            return "S"
""", ns)
    test_sequence_then_mapping = ns['test_sequence_then_mapping']
    test_mapping_then_sequence = ns['test_mapping_then_sequence']

    __doc__ = """
    >>> test_mapping_then_sequence(IsSequence())
    'S'
    >>> test_mapping_then_sequence(IsSequenceInheritsNeither())
    'S'
    >>> test_mapping_then_sequence(IsSequenceInheritsMapping())
    'S'
    >>> test_mapping_then_sequence(IsSequenceInheritsSequence())
    'S'
    >>> test_sequence_then_mapping(IsMapping())
    'M'
    >>> test_sequence_then_mapping(IsMappingInheritsNeither())
    'M'
    >>> test_sequence_then_mapping(IsMappingInheritsSequence())
    'M'
    >>> test_sequence_then_mapping(IsMappingInheritsMapping())
    'M'
    >>> test_sequence_then_mapping(Neither())
    """
