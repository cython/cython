cimport cython

cdef class Packet:
    cdef public object link
    cdef public object ident
    cdef public object kind
    cdef public Py_ssize_t datum
    cdef public list data

    cpdef append_to(self,lst)

cdef class TaskRec:
    pass

cdef class DeviceTaskRec(TaskRec):
    cdef public object pending

cdef class IdleTaskRec(TaskRec):
    cdef public long control
    cdef public Py_ssize_t count

cdef class HandlerTaskRec(TaskRec):
    cdef public object work_in   # = None
    cdef public object device_in # = None

    cpdef workInAdd(self,p)
    cpdef deviceInAdd(self,p)

cdef class WorkerTaskRec(TaskRec):
    cdef public object destination # = I_HANDLERA
    cdef public Py_ssize_t count

cdef class TaskState:
    cdef public bint packet_pending # = True
    cdef public bint task_waiting   # = False
    cdef public bint task_holding   # = False

    cpdef packetPending(self)
    cpdef waiting(self)
    cpdef running(self)
    cpdef waitingWithPacket(self)
    cpdef bint isPacketPending(self)
    cpdef bint isTaskWaiting(self)
    cpdef bint isTaskHolding(self)
    cpdef bint isTaskHoldingOrWaiting(self)
    cpdef bint isWaitingWithPacket(self)

cdef class TaskWorkArea:
    cdef public list taskTab # = [None] * TASKTABSIZE

    cdef public object taskList # = None

    cdef public Py_ssize_t holdCount # = 0
    cdef public Py_ssize_t qpktCount # = 0

cdef class Task(TaskState):
    cdef public Task link # = taskWorkArea.taskList
    cdef public object ident # = i
    cdef public object priority # = p
    cdef public object input # = w
    cdef public object handle # = r

    cpdef addPacket(self,Packet p,old)
    cpdef runTask(self)
    cpdef waitTask(self)
    cpdef hold(self)
    cpdef release(self,i)
    cpdef qpkt(self,Packet pkt)
    cpdef findtcb(self,id)

cdef class DeviceTask(Task):
    @cython.locals(d=DeviceTaskRec)
    cpdef fn(self,Packet pkt,r)

cdef class HandlerTask(Task):
    @cython.locals(h=HandlerTaskRec)
    cpdef fn(self,Packet pkt,r)

cdef class IdleTask(Task):
    @cython.locals(i=IdleTaskRec)
    cpdef fn(self,Packet pkt,r)

cdef class WorkTask(Task):
    @cython.locals(w=WorkerTaskRec)
    cpdef fn(self,Packet pkt,r)

@cython.locals(t=Task)
cpdef schedule()

cdef class Richards:
    cpdef run(self, iterations)
