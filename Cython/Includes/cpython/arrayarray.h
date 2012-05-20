/* arrayarray.h  

    artificial C-API for Python's 
    <array.array> type.
    copy this file to your -I path, e.g. .../pythonXX/include
    See array.pxd next to this file
    
    last changes: 2009-05-15 rk
                  2012-05-02 andreasvc

*/

#ifndef _ARRAYARRAY_H
#define _ARRAYARRAY_H

#include <Python.h>

struct arrayobject; /* Forward */

/* All possible arraydescr values are defined in the vector "descriptors"
 * below.  That's defined later because the appropriate get and set
 * functions aren't visible yet.
 */
typedef struct arraydescr {
    int typecode;
    int itemsize;
    PyObject * (*getitem)(struct arrayobject *, Py_ssize_t);
    int (*setitem)(struct arrayobject *, Py_ssize_t, PyObject *);
#if PY_VERSION_HEX >= 0x03000000
    char *formats;
#endif    
} arraydescr;


typedef struct arrayobject {
    PyObject_HEAD
    union {
        Py_ssize_t ob_size, length;
    };
    union {
        char *ob_item;
        float *_f;
        double *_d;
        int *_i;
        unsigned *_I;
        unsigned char *_B;
        signed char *_b;
        char *_c;
        unsigned long *_L;
        long *_l;
        short *_h;
        unsigned short *_H;
        Py_UNICODE *_u;
        void *_v;
    };
#if PY_VERSION_HEX >= 0x02040000
    Py_ssize_t allocated;
#endif
    struct arraydescr *ob_descr;
#if PY_VERSION_HEX >= 0x02040000
    PyObject *weakreflist; /* List of weak references */
#if PY_VERSION_HEX >= 0x03000000
        int ob_exports;  /* Number of exported buffers */
#endif
#endif
} arrayobject;


#ifndef NO_NEWARRAY_INLINE
/* 
 * 
 *  fast creation of a new array
 */
 
inline PyObject * newarrayobject(PyTypeObject *type, Py_ssize_t size,
    struct arraydescr *descr) {
    arrayobject *op;
    size_t nbytes;

    if (size < 0) {
        PyErr_BadInternalCall();
        return NULL;
    }

    nbytes = size * descr->itemsize;
    /* Check for overflow */
    if (nbytes / descr->itemsize != (size_t)size) {
        return PyErr_NoMemory();
    }
    op = (arrayobject *) type->tp_alloc(type, 0);
    if (op == NULL) {
        return NULL;
    }
    op->ob_descr = descr;
#if !( PY_VERSION_HEX < 0x02040000 )
    op->allocated = size;
    op->weakreflist = NULL;
#endif
    Py_SIZE(op) = size;
    if (size <= 0) {
        op->ob_item = NULL;
    }
    else {
        op->ob_item = PyMem_NEW(char, nbytes);
        if (op->ob_item == NULL) {
            Py_DECREF(op);
            return PyErr_NoMemory();
        }
    }
    return (PyObject *) op;
}
#else
PyObject* newarrayobject(PyTypeObject *type, Py_ssize_t size,
    struct arraydescr *descr);
#endif /* ifndef NO_NEWARRAY_INLINE */

/* fast resize (reallocation to the point) 
   not designed for filing small increments (but for fast opaque array apps) */
int resize(arrayobject *self, Py_ssize_t n) {
    void *item=self->ob_item;
    PyMem_Resize(item, char, (size_t)(n * self->ob_descr->itemsize));
    if (item == NULL) {
        PyErr_NoMemory();
        return -1;
    }    
    self->ob_item = item;
    self->ob_size = n;
#if PY_VERSION_HEX >= 0x02040000
    self->allocated = n;
#endif
    return 0;
}

/* suitable for small increments; over allocation 50% ;
   Remains non-smart in Python 2.3- ; but exists for compatibility */
int resize_smart(arrayobject *self, Py_ssize_t n) {
#if PY_VERSION_HEX >= 0x02040000
    void *item=self->ob_item;
    Py_ssize_t newsize;
    if (n < self->allocated) {
        if (n*4 > self->allocated) {
            self->ob_size = n;
            return 0;
        }
    }
    newsize = n  * 3 / 2 + 1;
    PyMem_Resize(item, char, (size_t)(newsize * self->ob_descr->itemsize));
    if (item == NULL) {
        PyErr_NoMemory();
        return -1;
    }    
    self->ob_item = item;
    self->ob_size = n;
    self->allocated = newsize;
    return 0;
#else
    return resize(self, n)   /* Python 2.3 has no 'allocated' */
#endif
}


#endif
/* _ARRAYARRAY_H */
