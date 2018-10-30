//////////////// Capsule.proto ////////////////

/* Todo: wrap the rest of the functionality in similar functions */
static CYTHON_INLINE PyObject *__pyx_capsule_create(void *p, const char *sig);

//////////////// Capsule ////////////////

static CYTHON_INLINE PyObject *
__pyx_capsule_create(void *p, const char *sig)
{
    return PyCapsule_New(p, sig, NULL);
}
