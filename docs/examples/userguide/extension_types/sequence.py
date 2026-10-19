@cython.collection_type("sequence")
@cython.cclass
class Range5:
    # be sure to define the sequence methods!
    def __len__(self):
        return 5
    def __getitem__(self, index):
        return index
