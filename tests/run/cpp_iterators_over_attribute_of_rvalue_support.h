#include <vector>

class HasIterableAttribute {
public:
    std::vector<int> vec;
    HasIterableAttribute() {
        for (int i = 1; i<=3; i++)
            vec.push_back(i);
    }
    HasIterableAttribute(std::vector<int> vec) : vec(vec) {}
};
