from cython.cimports import cqueue
from cython import cast

@cython.cclass
class Queue:
    """A queue class for C integer values.

    >>> q = Queue()
    >>> q.append(5)
    >>> q.peek()
    5
    >>> q.pop()
    5
    """
    _c_queue = cython.declare(cython.pointer[cqueue.Queue])
    def __cinit__(self):
        self._c_queue = cqueue.queue_new()
        if self._c_queue is cython.NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self._c_queue is not cython.NULL:
            cqueue.queue_free(self._c_queue)

    @cython.ccall
    def append(self, value: cython.int):
        if not cqueue.queue_push_tail(self._c_queue,
                cast(cython.p_void, cast(cython.Py_ssize_t, value))):
            raise MemoryError()

    # The `cpdef` feature is obviously not available for the original "extend()"
    # method, as the method signature is incompatible with Python argument
    # types (Python does not have pointers).  However, we can rename
    # the C-ish "extend()" method to e.g. "extend_ints()", and write
    # a new "extend()" method that provides a suitable Python interface by
    # accepting an arbitrary Python iterable.
    @cython.ccall
    def extend(self, values):
        for value in values:
            self.append(value)

    @cython.cfunc
    def extend_ints(self, values: cython.p_int, count: cython.size_t):
        value: cython.int
        for value in values[:count]:  # Slicing pointer to limit the iteration boundaries.
            self.append(value)

    @cython.ccall
    @cython.exceptval(-1, check=True)
    def peek(self) -> cython.int:
        value: cython.int = cast(cython.Py_ssize_t, cqueue.queue_peek_head(self._c_queue))

        if value == 0:
            # this may mean that the queue is empty,
            # or that it happens to contain a 0 value
            if cqueue.queue_is_empty(self._c_queue):
                raise IndexError("Queue is empty")
        return value

    @cython.ccall
    @cython.exceptval(-1, check=True)
    def pop(self) -> cython.int:
        if cqueue.queue_is_empty(self._c_queue):
            raise IndexError("Queue is empty")
        return cast(cython.Py_ssize_t, cqueue.queue_pop_head(self._c_queue))

    def __bool__(self):
        return not cqueue.queue_is_empty(self._c_queue)
