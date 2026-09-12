# mode: run
# tag: cpp, no-cpp-locals

# Shadow Python 'list' with C++ 'std::list'
from libcpp.list cimport list


cdef class LineAccumulator:
    """
    >>> la = LineAccumulator()
    >>> la.get_lines()
    [5.0]

    >>> import pickle
    >>> la2 = pickle.loads(pickle.dumps(la))
    >>> la2.get_lines()
    [5.0]
    """
    cdef list[double] lines

    def __init__(self):
        self.lines.push_back(5.0)

    def get_lines(self):
        return self.lines
