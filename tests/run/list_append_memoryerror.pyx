# mode: run
# tag: listcomp, comprehension, pep448

"""
>>> import sys
>>> def references_lost(build):
...     holder = Holder()
...     keep = [holder.item] * 10  # a release too many shows in the count
...     before = sys.getrefcount(holder.item)
...     set_fail_append(True)
...     try:
...         build(holder)
...     except MemoryError:
...         pass
...     finally:
...         set_fail_append(False)
...     return before - sys.getrefcount(holder.item)

>>> references_lost(listcomp)
0
>>> references_lost(merged_list)
0
"""

cdef extern from *:
    """
    static int fail_append = 0;
    static int failing_list_append(PyObject *list, PyObject *item) {
        if (fail_append) {
            PyErr_NoMemory();
            return -1;
        }
        return PyList_Append(list, item);
    }
    #define PyList_Append(list, item) failing_list_append(list, item)
    """
    int fail_append


def set_fail_append(bint value):
    global fail_append
    fail_append = value


class Holder:
    def __init__(self):
        self.item = object()


def listcomp(holder):
    return [holder.item for _ in range(3)]


def merged_list(holder):
    items = []
    return [*items, holder.item]
