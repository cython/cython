# mode: run
# cython: profile=True, binding=True

cpdef is_wrapper_profiled_separately():
    """
    >>> import tempfile, cProfile, pstats
    >>> statsFile = tempfile.mkstemp()[1]
    >>> cProfile.runctx('is_wrapper_profiled_separately()', globals(), locals(), statsFile);
    >>> s = pstats.Stats(statsFile)
    >>> for k in s.stats.keys():
    ...    func_name = k[2]
    ...    if '(wrapper)' in func_name:
    ...        print(func_name)   
    is_wrapper_profiled_separately (wrapper)
    """
    some_code = 1
