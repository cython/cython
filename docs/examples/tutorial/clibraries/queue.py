from cython.cimports import cqueue

@cython.cclass
class Queue:
    _c_queue = cython.declare(cython.pointer(cqueue.Queue))

    def __init__(self):
        self._c_queue = cqueue.queue_new()
