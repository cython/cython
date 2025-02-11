# mode: run
# tag: cpp, werror, no-cpp-locals
# ticket: 3065

# This is intentionally in a file on its own. The issue was that it failed to generate utility-code
# and so putting it with the other c++ exception checks wouldn't be a useful test

cdef extern from *:
    """
    #include <stdexcept>

    void cppf(int raiseCpp) {
        if (raiseCpp) {
            throw std::runtime_error("cpp");
        } else {
            PyErr_SetString(PyExc_RuntimeError, "py");
        }
    }
    """
    void cppf(int) except+*


def callcppf(int raiseCpp):
    """
    >>> callcppf(0)
    py
    >>> callcppf(1)
    cpp
    """
    try:
        cppf(raiseCpp)
    except RuntimeError as e:
        print(e.args[0])
