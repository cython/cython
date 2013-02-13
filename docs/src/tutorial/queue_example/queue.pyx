cimport cqueue

cdef class Queue:

    cdef cqueue.Queue* _c_queue

    def __cinit__(self):
        self._c_queue = cqueue.queue_new()
        if self._c_queue is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self._c_queue is not NULL:
            cqueue.queue_free(self._c_queue)

    cpdef int append(self, int value) except -1:
        if not cqueue.queue_push_tail(self._c_queue, <void*>value):
            raise MemoryError()
        return 0

    cdef int extend(self, int* values, Py_ssize_t count) except -1:
        cdef Py_ssize_t i
        for i in range(count):
            if not cqueue.queue_push_tail(self._c_queue, <void*>values[i]):
                raise MemoryError()
        return 0

    cpdef int peek(self) except? 0:
        cdef int value = <int>cqueue.queue_peek_head(self._c_queue)
        if value == 0:
            # this may mean that the queue is empty, or that it
            # happens to contain a 0 value
            if cqueue.queue_is_empty(self._c_queue):
                raise IndexError("Queue is empty")
        return value

    cpdef int pop(self) except? 0:
        cdef int value = <int>cqueue.queue_pop_head(self._c_queue)
        if value == 0:
            # this may mean that the queue is empty, or that it
            # happens to contain a 0 value
            if cqueue.queue_is_empty(self._c_queue):
                raise IndexError("Queue is empty")
        return value

    def __bool__(self):    # same as __nonzero__ in Python 2.x
        return not cqueue.queue_is_empty(self._c_queue)

DEF repeat_count=10000

def test_cy():
    cdef int i
    cdef Queue q = Queue()
    for i in range(repeat_count):
        q.append(i)
    for i in range(repeat_count):
        q.peek()
    while q:
        q.pop()

def test_py():
    cdef int i
    q = Queue()
    for i in range(repeat_count):
        q.append(i)
    for i in range(repeat_count):
        q.peek()
    while q:
        q.pop()

from collections import deque

def test_deque():
    cdef int i
    q = deque()
    for i in range(repeat_count):
        q.appendleft(i)
    for i in range(repeat_count):
        q[-1]
    while q:
        q.pop()

repeat = range(repeat_count)

def test_py_exec():
    q = Queue()
    d = dict(q=q, repeat=repeat)

    exec u"""\
for i in repeat:
    q.append(9)
for i in repeat:
    q.peek()
while q:
    q.pop()
""" in d
