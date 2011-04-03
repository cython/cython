/* A set of mutually incompatable return types. */

struct short_return { const char *msg; };
struct int_return { const char *msg; };
struct longlong_return { const char *msg; };

/* A set of overloaded methods. */

short_return f(short arg) {
    short_return val;
    val.msg = "short called";
    return val;
}

int_return f(int arg) {
    int_return val;
    val.msg = "int called";
    return val;
}

longlong_return f(long long arg) {
    longlong_return val;
    val.msg = "long long called";
    return val;
}
 
 
