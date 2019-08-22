class Base {
public:
    int foo(double a) {
        return (int) (a+0.5);
    }
    int foo(double* a) {
      return (int) (*a+0.5) - 1;
    }
};
