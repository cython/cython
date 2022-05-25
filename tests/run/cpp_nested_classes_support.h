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
  typedef int my_int;
  static my_int negate(my_int x) {
    return -x;
  }
};

template <typename T>
class TypedClass {
public:
  enum MyEnum {
    value = 39
  };
  union MyUnion {
    T typed_value;
    int int_value;
  };
  struct MyStruct {
    T typed_value;
    int int_value;
  };
  typedef T MyType;
};

class SpecializedTypedClass : public TypedClass<double> {};
