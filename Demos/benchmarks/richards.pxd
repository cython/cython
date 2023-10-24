cimport cython

@cython.final
cdef class Packet:
    pub object link
    pub object ident
    pub object kind
    pub isize datum
    pub list data

    cpdef append_to(self, lst)

cdef class TaskRec:
    pass

@cython.final
cdef class DeviceTaskRec(TaskRec):
    pub object pending

@cython.final
cdef class IdleTaskRec(TaskRec):
    pub i64 control
    pub isize count

@cython.final
cdef class HandlerTaskRec(TaskRec):
    pub object work_in   # = None
    pub object device_in # = None

    cpdef work_in_add(self, Packet p)
    cpdef device_in_add(self, Packet p)

@cython.final
cdef class WorkerTaskRec(TaskRec):
    pub object destination # = I_HANDLERA
    pub isize count

cdef class TaskState:
    pub bint packet_pending # = True
    pub bint task_waiting   # = False
    pub bint task_holding   # = False

    cpdef packet_pending(self)
    cpdef waiting(self)
    cpdef running(self)
    cpdef waiting_with_packet(self)
    cpdef bint is_packet_pending(self)
    cpdef bint is_task_waiting(self)
    cpdef bint is_task_holding(self)
    cpdef bint is_task_holding_or_waiting(self)
    cpdef bint is_waiting_with_packet(self)

cdef class TaskWorkArea:
    pub list taskTab # = [None] * TASKTABSIZE

    pub object taskList # = None

    pub isize hold_count # = 0
    pub isize qpkt_count # = 0

cdef class Task(TaskState):
    pub Task link # = taskWorkArea.taskList
    pub object ident # = i
    pub object priority # = p
    pub object input # = w
    pub object handle # = r

    cpdef add_packet(self, Packet p, Task old)
    cpdef run_task(self)
    cpdef wait_task(self)
    cpdef hold(self)
    cpdef release(self, i)
    cpdef qpkt(self, Packet pkt)
    cpdef findtcb(self, id)

cdef class DeviceTask(Task):
    @cython.locals(d=DeviceTaskRec)
    cpdef r#fn(self, Packet pkt, DeviceTaskRec r)

cdef class HandlerTask(Task):
    @cython.locals(h=HandlerTaskRec)
    cpdef r#fn(self, Packet pkt, HandlerTaskRec r)

cdef class IdleTask(Task):
    @cython.locals(i=IdleTaskRec)
    cpdef r#fn(self, Packet pkt, IdleTaskRec r)

cdef class WorkTask(Task):
    @cython.locals(w=WorkerTaskRec)
    cpdef r#fn(self, Packet pkt, WorkerTaskRec r)

@cython.locals(t=Task)
cpdef schedule()

cdef class Richards:
    cpdef run(self, iterations)
