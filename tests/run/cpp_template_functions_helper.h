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
};
