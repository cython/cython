#ifdef __cplusplus
extern "C" {
#endif
extern char *cp;
extern char *cpa[5];
extern int (*ifnpa[5])(void);
extern char *(*cpfnpa[5])(void);
extern int (*ifnp)(void);
extern int (*iap)[5];
#ifdef __cplusplus
}
#endif

char *cp;
char *cpa[5];
int (*ifnpa[5])(void);
char *(*cpfnpa[5])(void);
int (*ifnp)(void);
int (*iap)[5];



#ifdef __cplusplus
extern "C" {
#endif
extern DL_EXPORT(int) ifn(void);
extern DL_EXPORT(char *) cpfn(void);
extern DL_EXPORT(int) fnargfn(int (void));
extern DL_EXPORT(int) (*iapfn(void))[5];
extern DL_EXPORT(char *)(*cpapfn(void))[5];
#ifdef __cplusplus
}
#endif

int ifn(void) {return 0;}
char *cpfn(void) {return 0;}
int fnargfn(int f(void)) {return 0;}



#ifdef __cplusplus
extern "C" {
#endif
extern int ia[];
extern int iaa[][3];
extern DL_EXPORT(int) a(int[][3], int[][3][5]);
#ifdef __cplusplus
}
#endif

int ia[1];
int iaa[1][3];
int a(int a[][3], int b[][3][5]) {return 0;}
