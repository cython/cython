# mode: run
# tag: cpp, cpp11

#cython: test_fail_if_c_code_has = __Pyx_RefNannySetupContext\("call_a_method_with_an_error_return"
##cython: test_fail_if_c_code_has = /int __pyx_f_31gil_in_var_initialization_tests_1C_call_a_method_with_an_error_return\(.+{/:/__pyx_vtab/PyGILState_Ensure
#cython: test_fail_if_c_code_has = __Pyx_RefNannySetupContext\("call_me"
##cython: test_fail_if_c_code_has = /void __pyx_f_31gil_in_var_initialization_tests_1D_call_me\(.+{/:/get_left_edge\(/PyGILState_Ensure

# patterns above look for unwanted __Pyx_RefNannySetupContext and PyGILState_Ensure calls within
# the introductory part of the two functions (defined by looking at the function name, looking for
# a { to know we're at the function definition, and looking for a distinctive early line in the
# function.
# The second ones are disabled because they are tripped up by the annotated HTML output, where
# the code is jumbled up so they get caught by some GIL use in some unrelated error handling.

from libcpp cimport bool

# What we're testing in this file is that certain bits of code don't acquire the GIL
# at any point during the function.
#
# To do this we create a C++ thread that runs with the GIL permanently held, and
# which is waiting for a condition variable to be set. We run the relevant Cython
# function and then set the condition variable.
#
# If the Cython function requires the GIL it will be blocked by the C++ thread and
# so be unable to set the condition variable.
#
# This isn't specifically a C++ test, but the C++ standard library concurrency tools
# are a convenient way of getting condition variables and mutexes.

cdef extern from *:
    """
    #include <condition_variable>
    #include <mutex>
    #include <chrono>
    #include <future>

    static bool waiting = false;
    static bool triggered = false;
    static std::condition_variable condition_variable;
    static std::mutex mutex;

    void reset_cpp_state() {
        std::unique_lock<std::mutex> lock(mutex);
        waiting = false;
        triggered = false;
    }

    bool block_and_wait_for_trigger() {
        std::unique_lock<std::mutex> lock(mutex);
        waiting = true;
        triggered = false;
        condition_variable.notify_all();
        // Note - I'm using a 5 second timeout here to avoid the test
        // being "deadlock forever". This could occasionally give false
        // failures if things are running really slowly
        return condition_variable.wait_for(
            lock,
            std::chrono::seconds(5),
            []() {
                return triggered;
            });
    }

    void wait_for_waiting() {
        std::unique_lock<std::mutex> lock(mutex);
        condition_variable.wait(
            lock,
            []() {
                return waiting;
            });
    }

    void set_triggered() {
        std::unique_lock<std::mutex> lock(mutex);
        triggered = true;
        condition_variable.notify_all();
    }

    using bool_future = std::future<bool>;

    std::future<bool> run_block_and_wait_with_gil() {
        reset_cpp_state();
        return std::async(std::launch::async,
            [](){
                PyGILState_STATE gstate;
                gstate = PyGILState_Ensure();

                auto result = block_and_wait_for_trigger();

                PyGILState_Release(gstate);

                return result;
            });
    }
    """
    void wait_for_waiting() nogil
    void set_triggered() nogil
    cppclass bool_future:
        bool get() nogil
    bool_future run_block_and_wait_with_gil() nogil

cdef class C:
    cdef int some_c_method(self) except -1 nogil:
        return 0

    cdef int call_a_method_with_an_error_return(self) except -1 nogil:
        return self.some_c_method()

def test_method_with_error_return():
    """
    >>> test_method_with_error_return()
    """
    future = run_block_and_wait_with_gil()
    c = C()
    with nogil:
        wait_for_waiting()  # make sure the C++ thread has started and is holding the GIL
        c.call_a_method_with_an_error_return()
        set_triggered()
    assert future.get()


cdef inline float[:] _get_left_edge(float[::1] arr) nogil:
    return arr[:3]

cdef class D:
    cdef float _a
    def __cinit__(self, float a):
        self._a = a

    cdef void call_me(self, float[::1] my_arr) noexcept nogil:
        cdef Py_ssize_t idx
        cdef float[:] my_arr2 = _get_left_edge(my_arr)
        for idx in range(my_arr2.shape[0]):
            my_arr2[idx] = self._a

def test_method_with_memoryview_handling():
    """
    >>> test_method_with_memoryview_handling()
    """
    cdef float[10] static_arr
    cdef float[::1] view_of_static_arr = <float[:10:1]>static_arr
    future = run_block_and_wait_with_gil()
    d = D(5.)
    with nogil:
        wait_for_waiting()  # make sure the C++ thread has started and is holding the GIL
        d.call_me(view_of_static_arr)
        set_triggered()
    assert future.get()
