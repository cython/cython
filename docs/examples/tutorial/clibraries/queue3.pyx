cimport cqueue

cdef class Queue:
    """A queue class for C integer values.

    >>> q = Queue()
    >>> q.append(5)
    >>> q.peek()
    5
    >>> q.pop()
    5
    """
    cdef cqueue.Queue* _c_queue
    def __cinit__(self):
        self._c_queue = cqueue.queue_new()
        if self._c_queue is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self._c_queue is not NULL:
            cqueue.queue_free(self._c_queue)

    cpdef append(self, i32 value):
        if not cqueue.queue_push_tail(self._c_queue,
                                      <void*> <isize> value):
            raise MemoryError()

    # The `cpdef` feature is obviously not available for the original "extend()"
    # method, as the method signature is incompatible with Python argument
    # types (Python does not have pointers).  However, we can rename
    # the C-ish "extend()" method to e.g. "extend_ints()", and write
    # a new "extend()" method that provides a suitable Python interface by
    # accepting an arbitrary Python iterable.

    cpdef extend(self, values):
        for value in values:
            self.append(value)

    fn extend_ints(self, i32* values, usize count):
        let i32 value
        for value in values[:count]:  # Slicing pointer to limit the iteration boundaries.
            self.append(value)

    cpdef i32 peek(self) except? -1:
        let i32 value = <isize>cqueue.queue_peek_head(self._c_queue)

        if value == 0:
            # this may mean that the queue is empty,
            # or that it happens to contain a 0 value
            if cqueue.queue_is_empty(self._c_queue):
                raise IndexError("Queue is empty")
        return value

    cpdef i32 pop(self) except? -1:
        if cqueue.queue_is_empty(self._c_queue):
            raise IndexError("Queue is empty")
        return <isize>cqueue.queue_pop_head(self._c_queue)

    def __bool__(self):
        return not cqueue.queue_is_empty(self._c_queue)
