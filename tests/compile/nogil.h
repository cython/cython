#ifdef __cplusplus
extern "C" {
#endif
extern DL_EXPORT(void) e1(void);
extern DL_EXPORT(void *) e2(void);
#ifdef __cplusplus
}
#endif

void e1(void) {return;}
void *e2(void) {return 0;}



#ifdef __cplusplus
extern "C" {
#endif
extern DL_EXPORT(PyObject *) g(PyObject*);
extern DL_EXPORT(void) g2(PyObject*);
#ifdef __cplusplus
}
#endif

PyObject *g(PyObject* o) {return 0;}
void g2(PyObject* o) {return;}
