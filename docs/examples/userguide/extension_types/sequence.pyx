cimport cython

@cython.collection_type("sequence")
cdef class Range5:
    # be sure to define the sequence methods!
    def __len__(self):
        return 5
    def __getitem__(self, index):
        return index
