#include <Python.h>

typedef void (*cheesefunc)(char* name, void* user_data);
Py_EXPORTED_SYMBOL void find_cheeses(cheesefunc user_func, void* user_data);
