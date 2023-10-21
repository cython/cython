cimport cython

@cython.final
cdef class Packet:
    cdef pub object link
    cdef pub object ident
    cdef pub object kind
    cdef pub isize datum
    cdef pub list data

    cpdef append_to(self, lst)

cdef class TaskRec:
    pass

@cython.final
cdef class DeviceTaskRec(TaskRec):
    cdef pub object pending

@cython.final
cdef class IdleTaskRec(TaskRec):
    cdef pub i64 control
    cdef pub isize count

@cython.final
cdef class HandlerTaskRec(TaskRec):
    cdef pub object work_in   # = None
    cdef pub object device_in # = None

    cpdef work_in_add(self, Packet p)
    cpdef device_in_add(self, Packet p)

@cython.final
cdef class WorkerTaskRec(TaskRec):
    cdef pub object destination # = I_HANDLERA
    cdef pub isize count

cdef class TaskState:
    cdef pub bint packet_pending # = True
    cdef pub bint task_waiting   # = False
    cdef pub bint task_holding   # = False

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
    cdef pub list taskTab # = [None] * TASKTABSIZE

    cdef pub object taskList # = None

    cdef pub isize hold_count # = 0
    cdef pub isize qpkt_count # = 0

cdef class Task(TaskState):
    cdef pub Task link # = taskWorkArea.taskList
    cdef pub object ident # = i
    cdef pub object priority # = p
    cdef pub object input # = w
    cdef pub object handle # = r

    cpdef add_packet(self, Packet p, Task old)
    cpdef run_task(self)
    cpdef wait_task(self)
    cpdef hold(self)
    cpdef release(self, i)
    cpdef qpkt(self, Packet pkt)
    cpdef findtcb(self, id)

cdef class DeviceTask(Task):
    @cython.locals(d=DeviceTaskRec)
    cpdef f(self, Packet pkt, DeviceTaskRec r)

cdef class HandlerTask(Task):
    @cython.locals(h=HandlerTaskRec)
    cpdef f(self, Packet pkt, HandlerTaskRec r)

cdef class IdleTask(Task):
    @cython.locals(i=IdleTaskRec)
    cpdef f(self, Packet pkt, IdleTaskRec r)

cdef class WorkTask(Task):
    @cython.locals(w=WorkerTaskRec)
    cpdef f(self, Packet pkt, WorkerTaskRec r)

@cython.locals(t=Task)
cpdef schedule()

cdef class Richards:
    cpdef run(self, iterations)
