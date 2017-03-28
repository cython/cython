template <typename T>
T no_arg() {
    return T();
}

template <typename T>
T one_param(T value) {
    return value;
}

template <typename T, typename U>
std::pair<T, U> two_params(T a, U b) {
    return std::pair<T, U>(a, b);
}

template <typename T>
class A {
    public:
        template <typename U>
        std::pair<T, U> method(T a, U b) {
            return std::pair<T, U>(a, b);
        }
        template <typename U>
        U part_method(std::pair<T, U> p) {
            return p.second;
        }
        template <typename U>
        U part_method_ref(const std::pair<T, U>& p) {
            return p.second;
        }

        int overloaded(double d) {
            return (int) d;
        }
        T overloaded(std::pair<T, T> p) {
            return p.first;
        }
        template <typename U>
        U overloaded(std::vector<U> v) {
            return v[0];
        }
        template <typename U>
        U overloaded(char* c, std::vector<U> v) {
            return v[0];
        }
};

template <typename T>
T nested_deduction(const T *a) {
    return *a;
}

template <typename T, typename U>
std::pair<T, U> pair_arg(std::pair<T, U> a) {
    return a;
}

template <typename T>
T* pointer_param(T* param) {
    return param;
}

class double_pair : public std::pair<double, double> {
  public:
    double_pair(double x, double y) : std::pair<double, double>(x, y) { };
};
