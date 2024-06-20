//////////////////// MainFunction ////////////////////

#ifdef __FreeBSD__
#include <floatingpoint.h>
#endif

#if defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)
int %(wmain_method)s(int argc, wchar_t **argv)
#else
static int __Pyx_main(int argc, wchar_t **argv)
#endif
{
    /* 754 requires that FP exceptions run in "no stop" mode by default,
     * and until C vendors implement C99's ways to control FP exceptions,
     * Python requires non-stop mode.  Alas, some platforms enable FP
     * exceptions by default.  Here we disable them.
     */
#ifdef __FreeBSD__
    fp_except_t m;

    m = fpgetmask();
    fpsetmask(m & ~FP_X_OFL);
#endif
#if PY_VERSION_HEX < 0x03080000
    if (argc && argv)
        Py_SetProgramName(argv[0]);
#endif

    if (PyImport_AppendInittab("%(module_name)s", PyInit_%(module_name)s) < 0) return 1;

#if PY_VERSION_HEX < 0x03080000
    Py_Initialize();
    if (argc && argv)
        PySys_SetArgv(argc, argv);
#else
    {
        PyStatus status;

        PyConfig config;
        PyConfig_InitPythonConfig(&config);
        // Disable parsing command line arguments
        config.parse_argv = 0;

        if (argc && argv) {
            status = PyConfig_SetString(&config, &config.program_name, argv[0]);
            if (PyStatus_Exception(status)) {
                PyConfig_Clear(&config);
                return 1;
            }

            status = PyConfig_SetArgv(&config, argc, argv);
            if (PyStatus_Exception(status)) {
                PyConfig_Clear(&config);
                return 1;
            }
        }

        status = Py_InitializeFromConfig(&config);
        if (PyStatus_Exception(status)) {
            PyConfig_Clear(&config);
            return 1;
        }

        PyConfig_Clear(&config);
    }
#endif

    { /* init module '%(module_name)s' as '__main__' */
      PyObject* m = NULL;
      %(module_is_main)s = 1;
      m = PyImport_ImportModule("%(module_name)s");

      if (!m && PyErr_Occurred()) {
          PyErr_Print(); /* This exits with the right code if SystemExit. */
          return 1;
      }
      Py_XDECREF(m);
    }
    if (Py_FinalizeEx() < 0)
        return 2;
    return 0;
}


#if !defined(_WIN32) && !defined(WIN32) && !defined(MS_WINDOWS)
#include <locale.h>

int
%(main_method)s(int argc, char **argv)
{
    if (!argc) {
        return __Pyx_main(0, NULL);
    }
    else {
        int i, res;
        wchar_t **argv_copy = (wchar_t **)malloc(sizeof(wchar_t*)*argc);
        /* We need a second copy, as Python might modify the first one. */
        wchar_t **argv_copy2 = (wchar_t **)malloc(sizeof(wchar_t*)*argc);
        char *oldloc = strdup(setlocale(LC_ALL, NULL));
        if (!argv_copy || !argv_copy2 || !oldloc) {
            fprintf(stderr, "out of memory\\n");
            free(argv_copy);
            free(argv_copy2);
            free(oldloc);
            return 1;
        }
        res = 0;
        setlocale(LC_ALL, "");
        for (i = 0; i < argc; i++) {
            argv_copy2[i] = argv_copy[i] = Py_DecodeLocale(argv[i], NULL);
            if (!argv_copy[i]) res = 1;  /* failure, but continue to simplify cleanup */
        }
        setlocale(LC_ALL, oldloc);
        free(oldloc);
        if (res == 0)
            res = __Pyx_main(argc, argv_copy);
        for (i = 0; i < argc; i++) {
            PyMem_RawFree(argv_copy2[i]);
        }
        free(argv_copy);
        free(argv_copy2);
        return res;
    }
}
#endif
