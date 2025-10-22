#if defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

typedef void (*cheesefunc)(char *name, void *user_data);
DLL_EXPORT void find_cheeses(cheesefunc user_func, void *user_data);
