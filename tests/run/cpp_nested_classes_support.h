class A {
public:
  class B {
  public:
    int square(int x) { return x * x; }
    class C {
        public:
        int cube(int x) { return x * x * x; }
    };
  };
  B* createB() {
    return new B();
  }
};
