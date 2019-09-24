#include <unordered_map>

struct MyStruct {
    bool operator == (const MyStruct & rhs) const {
        return true;
    }
};

struct Hasher {
    std::size_t operator()(const MyStruct & val) const {
        return 0;
    }
};

std::unordered_map<MyStruct, int, Hasher> map_with_specific_hasher;
