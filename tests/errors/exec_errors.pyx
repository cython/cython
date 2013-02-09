# mode: error
# tag: exec

def test_exec_tuples():
    exec()
    exec(1,)
    exec(1,2,3,4)

def test_exec_tuples_with_in(d1, d2):
    exec(1,2) in d1
    exec(1,2,3) in d1
    exec(1,2) in d1, d2
    exec(1,2,3) in d1, d2


_ERRORS = """
 5:4: expected tuple of length 2 or 3, got length 0
 6:4: expected tuple of length 2 or 3, got length 1
 7:4: expected tuple of length 2 or 3, got length 4
10:14: tuple variant of exec does not support additional 'in' arguments
11:16: tuple variant of exec does not support additional 'in' arguments
12:14: tuple variant of exec does not support additional 'in' arguments
13:16: tuple variant of exec does not support additional 'in' arguments
"""
