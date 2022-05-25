/* A set of mutually incompatible return types. */

struct short_return { char *msg; };
struct int_return { char *msg; };
struct longlong_return { char *msg; };

/* A set of overloaded methods. */

short_return f(short arg) {
    short_return val;
    arg++;
    val.msg = (char*)"short called";
    return val;
}

int_return f(int arg) {
    int_return val;
    arg++;
    val.msg = (char*)"int called";
    return val;
}

longlong_return f(long long arg) {
    longlong_return val;
    arg++;
    val.msg = (char*)"long long called";
    return val;
}
 
 
