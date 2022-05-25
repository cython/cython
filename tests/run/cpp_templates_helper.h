template <typename T, typename S=T, typename U=T>
class Wrap {
    T value;
public:
    typedef S AltType;

    Wrap(T v) : value(v) { }
    void set(T v) { value = v; }
    T get(void) { return value; }
    bool operator==(Wrap<T> other) { return value == other.value; }

    S get_alt_type(void) { return (S) value; }
    void set_alt_type(S v) { value = (T) v; }

    U create(void) { return (U) value; }
    bool accept(U v) { return v == (U) value; }
};

template <class T1, class T2>
class Pair {
    T1 _first;
    T2 _second;
public:
    Pair() { }
    Pair(T1 u, T2 v) { _first = u; _second = v; }
    T1 first(void) { return _first; }
    T2 second(void) { return _second; }
    bool operator==(Pair<T1,T2> other) { return _first == other._first && _second == other._second; }
    bool operator!=(Pair<T1,T2> other) { return _first != other._first || _second != other._second; }
};

template <class T1, class T2>
class SuperClass {
public:
    SuperClass() {}
};

template <class T2, class T3>
class SubClass : public SuperClass<T2, T3> {
};

template <class T>
class Div {
public:
    static T half(T value) { return value / 2; }
};

template <class T1, class T2>
class BinaryAnd {
public:
    static T1 call(T1 x, T2 y) { return x & y; }
};
