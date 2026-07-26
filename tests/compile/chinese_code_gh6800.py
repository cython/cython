# mode: compile

# As presented in https://github.com/cython/cython/issues/6800

# This is a pure compile test for non-Latin names.

import psutil

def 关闭进程(进程pid,超时=None):
    try:
        进程对象 = psutil.Process(进程pid)
    except psutil.TimeoutExpired:
        if 进程对象.is_running():进程对象.kill();进程对象.wait()
