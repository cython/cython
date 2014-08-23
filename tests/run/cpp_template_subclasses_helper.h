using namespace std;

class Base {
public:
    virtual const char* name() { return "Base"; }
    virtual ~Base() {}
};

template <class A1>
class A : public Base {
public:
    virtual const char* name() { return "A"; }
    A1 funcA(A1 x) { return x; }
};

template <class B1, class B2>
class B : public A<B2> {
public:
    virtual const char* name() { return "B"; }
    pair<B1, B2> funcB(B1 x, B2 y) { return pair<B1, B2>(x, y); }
};

template <class C1>
class C : public B<long, C1> {
public:
    virtual const char* name() { return "C"; }
    C1 funcC(C1 x) { return x; }
};

template <class D1>
class D : public C<pair<D1, D1> > {
    virtual const char* name() { return "D"; }
};

class E : public D<double> {
    virtual const char* name() { return "E"; }
};
