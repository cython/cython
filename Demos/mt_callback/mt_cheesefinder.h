#ifndef MT_CHEESES_C_CB_H
#define MT_CHEESES_C_CB_H
/* 
** This file contains c-callbacks called from the C-code as well as from Python-code
*/


//C function implmented in cython. called from the c-code e.g. mytest.c 
extern int cheeses_action_handler(char *cheese_name, void *user_data);

//C function implmented in c-lib . called from the python code e.g run_mt_cheeses.py
extern void cheeses_init_pthreads(void);

#endif
