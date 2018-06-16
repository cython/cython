# queue.pyx

from libc.stdint cimport intptr_t
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

    cpdef append(self, intptr_t value):
        if not cqueue.queue_push_tail(self._c_queue,
                                      <void*> value):
            raise MemoryError()

    cdef extend(self, intptr_t* values, size_t count):
        cdef size_t i
        for i in range(count):
            if not cqueue.queue_push_tail(
                    self._c_queue, <void*> values[i]):
                raise MemoryError()

    # The `cpdef` feature is obviously not available for the `extend()`
    # method, as the method signature is incompatible with Python argument
    # types (Python doesn't have pointers). However, we can make a method
    # called `extend_python` instead that accepts an arbitrary Python iterable.
    cpdef extend_python(self, values):
        for value in values:
            self.append(value)

    cpdef intptr_t peek(self) except? -1:
        cdef intptr_t value = <intptr_t> cqueue.queue_peek_head(self._c_queue)

        if value == 0:
            # this may mean that the queue is empty,
            # or that it happens to contain a 0 value
            if cqueue.queue_is_empty(self._c_queue):
                raise IndexError("Queue is empty")
        return value

    cpdef intptr_t pop(self) except? -1:
        if cqueue.queue_is_empty(self._c_queue):
            raise IndexError("Queue is empty")
        return <intptr_t> cqueue.queue_pop_head(self._c_queue)

    def __bool__(self):
        return not cqueue.queue_is_empty(self._c_queue)
