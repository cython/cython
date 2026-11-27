# mode: run
# tag: listcomp, comprehension, pep448

"""
Fail each allocation in turn until the call succeeds; a list item must not
lose a reference when appending it fails. The loop runs uncompiled, so that
only the functions under test allocate while allocations fail. Refnanny
allocates as well and then reports its own failures, so the check runs only
without it.

>>> import sys
>>> try:
...     from _testcapi import remove_mem_hooks, set_nomemory
... except ImportError:
...     set_nomemory = None
>>> def references_lost(build):
...     if set_nomemory is None or refnanny or not hasattr(sys, "getrefcount"):
...         return 0
...     holder = Holder()
...     keep = [holder.item] * 10  # a release too many shows in the count
...     before = sys.getrefcount(holder.item)
...     for allocation in range(100):
...         set_nomemory(allocation, allocation + 1)
...         try:
...             build(holder)
...         except MemoryError:
...             continue
...         finally:
...             remove_mem_hooks()
...         break
...     return before - sys.getrefcount(holder.item)

>>> references_lost(listcomp)
0
>>> references_lost(merged_list)
0
"""

cdef extern from *:
    """
    #if CYTHON_REFNANNY
    #define REFNANNY_ENABLED 1
    #else
    #define REFNANNY_ENABLED 0
    #endif
    """
    bint REFNANNY_ENABLED

refnanny = REFNANNY_ENABLED


class Holder:
    def __init__(self):
        self.item = object()


def listcomp(holder):
    return [holder.item for _ in range(3)]


def merged_list(holder):
    items = []
    return [*items, holder.item]
