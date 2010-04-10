#ifdef __cplusplus
extern "C" {
#endif
extern DL_EXPORT(int) f1(void);
extern DL_EXPORT(int) __cdecl f2(void);
extern DL_EXPORT(int) __stdcall f3(void);
extern DL_EXPORT(int) __fastcall f4(void);
#ifdef __cplusplus
}
#endif

int f1(void) {return 0;}
int __cdecl f2(void) {return 0;}
int __stdcall f3(void) {return 0;}
int __fastcall f4(void) {return 0;}



#ifdef __cplusplus
extern "C" {
#endif
extern int (*p1)(void);
extern int (__cdecl *p2)(void);
extern int (__stdcall *p3)(void);
extern int (__fastcall *p4)(void);
#ifdef __cplusplus
}
#endif

int (*p1)(void);
int (__cdecl *p2)(void);
int (__stdcall *p3)(void);
int (__fastcall *p4)(void);
