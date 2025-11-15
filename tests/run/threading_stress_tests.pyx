# mode: run

import threading

cdef int raises(int i) except -1:
    if i==0:
        raise RuntimeError()
    elif i==1:
        raise ValueError()
    elif i==2:
        raise AttributeError()
    elif i==3:
        raise TypeError()
    elif i==4:
        raise KeyError()
    else:
        raise SystemError()

def exception_test(num_threads):
    """
    >>> exception_test(4)
    """
    barrier = threading.Barrier(num_threads)
    results = []

    def runner():
        local_results = []
        barrier.wait()
        for _ in range(5):
            for i in range(6):
                try:
                    raises(i)
                except BaseException as e:
                    local_results.append(e)
        results.extend(local_results)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=runner)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # The main thread safety issue is out cache of stack frames.
    # Therefore, check that the line numbers are consistent.
    types_and_linenos = {}
    for r in results:
        tp = type(r)
        tb = r.__traceback__
        while tb.tb_next:
            tb = tb.tb_next
        lineno = tb.tb_lineno
        existing_lineno = types_and_linenos.setdefault(tp, lineno)
        assert existing_lineno == lineno, (tp, existing_lineno, lineno)
