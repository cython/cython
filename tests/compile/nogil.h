extern DL_EXPORT(void) e1(void);
extern DL_EXPORT(int*) e2(void);

void e1(void) {return;}
int* e2(void) {return 0;}



extern DL_EXPORT(PyObject *) g(PyObject*);
extern DL_EXPORT(void) g2(PyObject*);

PyObject *g(PyObject* o) {if (o) {}; return 0;}
void g2(PyObject* o) {if (o) {}; return;}
