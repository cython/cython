#
# Cython wrapper for multithreaded cheesefinder API
#

from threading import Thread
from multiprocessing.pool import ThreadPool

cdef extern from "mt_cheesefinder.h" nogil:
     void cheeses_init_pthreads()   

actions = dict();
pool = ThreadPool(processes=10)

#Function to initialize C side and start pthreads
cpdef cheeses_init() :
    print("Initializing C threads from python\n");
    cheeses_init_pthreads();
    
#register python callbacks to be called from the c side
def reg( action,func ):
    print ( "Action registered for %s" % (action));
    if action not in actions:
       actions[action] = dict();
    actions[action] = func;

#un-register python callbacks to be called from the c side
def unreg(action):
    del(actions[action]);
    if not actions[action]:
       del(actions[action]);

#python function calling the specified call-back
def action_handler( action ):
    if action in actions:
       async_result = pool.apply_async( actions[action] )
       return async_result.get()
    else:
       return 0

#c-function wrapping python function
cdef public int cheeses_action_handler(char *name, void *user_data) with gil:
    cdef int ret;
    ret  =  action_handler( name );
    return ret;

