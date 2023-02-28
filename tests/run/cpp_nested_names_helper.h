#ifndef CPP_NESTED_NAMES_HELPER_H
#define CPP_NESTED_NAMES_HELPER_H

#include <string>

struct Outer {
  struct Nested {
    struct NestedNested {
      std::string get_str() { return "NestedNested"; }
    };

    std::string get_str() { return "Nested"; }

    static NestedNested get() { return NestedNested(); }
  };

  static Nested get() { return Outer::Nested(); }
};

#endif
