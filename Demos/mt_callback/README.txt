Callback from C-Threads
------------------------
This project illustrates calling a python callback from a c-thread (posix) using cython as glue.
Since the Python interpreter is not aware of the c-threads , we need to create a Python thread state for each C-thread.
We achieve this in Cython by creating a Python thread-pool and map the callbacks coming in from the C-threads to the threads in the pool.

1. Makefile
   make all   - builds the C-extension python module by compiling the cython code and c-code .   
   make test  - performs 'make all'  and runs the test python module run_mt_cheeses.py

2. mt_cheeses_c_cb.h - contains c function declarations exported by mt_cheesefinder.c (c library) and mt_cheese.pyx ( cython library)
3. mt_cheeses.pyx - cython code defines c-functions to be called from c-code and calls python callbacks registered by python code. 
4. mt_cheesefinder.c - C library code which creates 10 pthreads and calls python functions through the c-extension exported by cython.
5. run_mt_cheeses.py - This is the sample Python code which implementes callback functions and registers with cython code , so that they could be called from mt_cheesefinder.c.
6. Setup.py  - Uses distutils to build cython code and c-code into python extension.

This code is built on top of Cython/Demos/callback in github. The example cheesefinder implements a callback from c , however this does not work
as-is when the callback is called from a posix thread for the reasons cited above in introduction.  
Hence I built this to illustrate the required changes.
