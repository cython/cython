//////////////////// MainFunction ////////////////////

#ifdef __FreeBSD__
#include <floatingpoint.h>
#endif

#if PY_MAJOR_VERSION < 3
int %(main_method)s(int argc, char** argv)
#elif defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)
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

    #if PY_MAJOR_VERSION < 3
    if (PyImport_AppendInittab("%(module_name)s", init%(module_name)s) < 0) return 1;
    #else
    if (PyImport_AppendInittab("%(module_name)s", PyInit_%(module_name)s) < 0) return 1;
    #endif

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
          #if PY_MAJOR_VERSION < 3
          if (Py_FlushLine()) PyErr_Clear();
          #endif
          return 1;
      }
      Py_XDECREF(m);
    }
#if PY_VERSION_HEX < 0x03060000
    Py_Finalize();
#else
    if (Py_FinalizeEx() < 0)
        return 2;
#endif
    return 0;
}


#if PY_MAJOR_VERSION >= 3 && !defined(_WIN32) && !defined(WIN32) && !defined(MS_WINDOWS)
#include <locale.h>

#if PY_VERSION_HEX < 0x03050000

static wchar_t*
__Pyx_char2wchar(char* arg)
{
    wchar_t *res;
#ifdef HAVE_BROKEN_MBSTOWCS
    /* Some platforms have a broken implementation of
     * mbstowcs which does not count the characters that
     * would result from conversion.  Use an upper bound.
     */
    size_t argsize = strlen(arg);
#else
    size_t argsize = mbstowcs(NULL, arg, 0);
#endif
    size_t count;
    unsigned char *in;
    wchar_t *out;
#ifdef HAVE_MBRTOWC
    mbstate_t mbs;
#endif
    if (argsize != (size_t)-1) {
        res = (wchar_t *)malloc((argsize+1)*sizeof(wchar_t));
        if (!res)
            goto oom;
        count = mbstowcs(res, arg, argsize+1);
        if (count != (size_t)-1) {
            wchar_t *tmp;
            /* Only use the result if it contains no
               surrogate characters. */
            for (tmp = res; *tmp != 0 &&
                     (*tmp < 0xd800 || *tmp > 0xdfff); tmp++)
                ;
            if (*tmp == 0)
                return res;
        }
        free(res);
    }
    /* Conversion failed. Fall back to escaping with surrogateescape. */
#ifdef HAVE_MBRTOWC
    /* Try conversion with mbrtwoc (C99), and escape non-decodable bytes. */

    /* Overallocate; as multi-byte characters are in the argument, the
       actual output could use less memory. */
    argsize = strlen(arg) + 1;
    res = (wchar_t *)malloc(argsize*sizeof(wchar_t));
    if (!res) goto oom;
    in = (unsigned char*)arg;
    out = res;
    memset(&mbs, 0, sizeof mbs);
    while (argsize) {
        size_t converted = mbrtowc(out, (char*)in, argsize, &mbs);
        if (converted == 0)
            /* Reached end of string; null char stored. */
            break;
        if (converted == (size_t)-2) {
            /* Incomplete character. This should never happen,
               since we provide everything that we have -
               unless there is a bug in the C library, or I
               misunderstood how mbrtowc works. */
            fprintf(stderr, "unexpected mbrtowc result -2\\n");
            free(res);
            return NULL;
        }
        if (converted == (size_t)-1) {
            /* Conversion error. Escape as UTF-8b, and start over
               in the initial shift state. */
            *out++ = 0xdc00 + *in++;
            argsize--;
            memset(&mbs, 0, sizeof mbs);
            continue;
        }
        if (*out >= 0xd800 && *out <= 0xdfff) {
            /* Surrogate character.  Escape the original
               byte sequence with surrogateescape. */
            argsize -= converted;
            while (converted--)
                *out++ = 0xdc00 + *in++;
            continue;
        }
        /* successfully converted some bytes */
        in += converted;
        argsize -= converted;
        out++;
    }
#else
    /* Cannot use C locale for escaping; manually escape as if charset
       is ASCII (i.e. escape all bytes > 128. This will still roundtrip
       correctly in the locale's charset, which must be an ASCII superset. */
    res = (wchar_t *)malloc((strlen(arg)+1)*sizeof(wchar_t));
    if (!res) goto oom;
    in = (unsigned char*)arg;
    out = res;
    while(*in)
        if(*in < 128)
            *out++ = *in++;
        else
            *out++ = 0xdc00 + *in++;
    *out = 0;
#endif
    return res;
oom:
    fprintf(stderr, "out of memory\\n");
    return NULL;
}

#endif

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
            argv_copy2[i] = argv_copy[i] =
#if PY_VERSION_HEX < 0x03050000
                __Pyx_char2wchar(argv[i]);
#else
                Py_DecodeLocale(argv[i], NULL);
#endif
            if (!argv_copy[i]) res = 1;  /* failure, but continue to simplify cleanup */
        }
        setlocale(LC_ALL, oldloc);
        free(oldloc);
        if (res == 0)
            res = __Pyx_main(argc, argv_copy);
        for (i = 0; i < argc; i++) {
#if PY_VERSION_HEX < 0x03050000
            free(argv_copy2[i]);
#else
            PyMem_RawFree(argv_copy2[i]);
#endif
        }
        free(argv_copy);
        free(argv_copy2);
        return res;
    }
}
#endif
