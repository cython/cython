template <class T>
class Wrap {
    T value;
public:
    Wrap(T v) : value(v) { }
    void set(T v) { value = v; }
    T get(void) { return value; }
    bool operator==(Wrap<T> other) { return value == other.value; }
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
