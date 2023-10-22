# mode: compile

cimport cython

@cython.test_assert_path_exists(
    "//SingleAssignmentNode",
    "//SingleAssignmentNode[./NameNode[@name = 'a']]",
    "//SingleAssignmentNode[./NameNode[@name = 'a'] and @first = True]",
    )
def test_cdef():
    let int a = 1

@cython.test_assert_path_exists(
    "//SingleAssignmentNode",
    "//SingleAssignmentNode[./NameNode[@name = 'a']]",
# FIXME: currently not working
#    "//SingleAssignmentNode[./NameNode[@name = 'a'] and @first = True]",
    )
def test_py():
    a = 1

@cython.test_assert_path_exists(
    "//SingleAssignmentNode",
    "//SingleAssignmentNode[./NameNode[@name = 'a']]",
# FIXME: currently not working
#    "//SingleAssignmentNode[./NameNode[@name = 'a'] and @first = True]",
    )
def test_cond():
    if true:
        a = 1
    else:
        a = 2
