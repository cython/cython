"""
>>> f()
hello from cython scope, value=4
hello from cython.view scope, value=4
hello from cython scope, value=3
hello from cython.view scope, value=3
>>> viewobjs()
<strided axis packing mode>
<contig axis packing mode>
<follow axis packing mode>
<direct axis access mode>
<ptr axis access mode>
<full axis access mode>
"""

cimport cython

from cython cimport _testscope as tester
from cython.view cimport _testscope as viewtester


def f():
    print cython._testscope(4)
    print cython.view._testscope(4)
    print tester(3)
    print viewtester(3)

def viewobjs():
    print cython.view.strided
    print cython.view.contig
    print cython.view.follow
    print cython.view.direct
    print cython.view.ptr
    print cython.view.full
