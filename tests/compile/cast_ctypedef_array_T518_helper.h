struct __foo_struct { int i, j; };
typedef struct __foo_struct foo_t[1];

static void foo_init  (foo_t v) { v[0].i = 0; v[0].j = 0; }
static void foo_clear (foo_t v) { v[0].i = 0; v[0].j = 0; }
