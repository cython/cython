#ifndef CPPWRAP_LIB_H
#define CPPWRAP_LIB_H
void voidfunc(void);

double doublefunc (double a, double b, double c);


class DoubleKeeper
{
    double number;

public:
    DoubleKeeper (double number);
    virtual ~DoubleKeeper ();

    void set_number (double num);
    double get_number () const;
    virtual double transmogrify (double value) const;
};

double transmogrify_from_cpp (DoubleKeeper const *obj, double value);
#endif
