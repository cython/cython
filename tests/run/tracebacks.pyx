# tag: traceback

def foo1():
  foo2()

cdef foo2():
  foo3()

cdef int foo3() except -1:
  raise RuntimeError('my_message')

def test_traceback(cline_in_traceback=None):
  """
  >>> test_traceback()
  >>> test_traceback(True)
  >>> test_traceback(False)
  """
  if cline_in_traceback is not None:
    import cython_runtime
    cython_runtime.cline_in_traceback = cline_in_traceback
  try:
    foo1()
  except:
    import traceback
    tb_string = traceback.format_exc()
    expected = (
      'tracebacks.pyx',
      'foo1', 'foo2', 'foo3',
      'line 4', 'line 7', 'line 10',
      'my_message')
    for s in expected:
      assert s in tb_string, s
    if cline_in_traceback:
      assert 'tracebacks.c' in tb_string
    else:
      assert 'tracebacks.c' not in tb_string
