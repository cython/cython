#if defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)
#define DLL_EXPORT __declspec(dllexport)
#endif

DLL_EXPORT double sinc(double);
