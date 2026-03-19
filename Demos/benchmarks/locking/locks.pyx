cimport cython

import threading
import random
import time

cdef fused LockT:
    cython.pymutex
    cython.pythread_type_lock

cdef void do_run(LockT *lock, int n_threads, int n_iter, double wait_probablility, double wait_time_ms, double idle_time_ms):
    barrier = threading.Barrier(n_threads)
    thread_counts = [0]*n_threads

    def thread_func(thread_num):
        generator = random.Random(thread_num)
        barrier.wait()
        while True:
            with lock[0]:
                thread_counts[thread_num] += 1
                if all(tc > n_iter for tc in thread_counts):
                    return
                r = generator.random()
                if r < wait_probablility and wait_time_ms != 0:
                    time.sleep(wait_time_ms*0.001)
            if idle_time_ms != 0:
                time.sleep(idle_time_ms*0.001)

    threads = [
        threading.Thread(target=thread_func, args=(n,)) for n in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(thread_counts)



def run(lock_type, int n_threads, int n_iter, double wait_probablility, double wait_time_ms, double idle_time_ms):
    cdef cython.pymutex m
    cdef cython.pythread_type_lock l
    if lock_type == "pymutex":
        do_run(&m, n_threads, n_iter, wait_probablility, wait_time_ms, idle_time_ms)
    else:
        do_run(&l, n_threads, n_iter, wait_probablility, wait_time_ms, idle_time_ms)
