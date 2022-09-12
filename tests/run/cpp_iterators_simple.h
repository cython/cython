class DoublePointerIter {
public:
    DoublePointerIter(double* start, int len) : start_(start), len_(len) { }
    double* begin() { return start_; }
    double* end() { return start_ + len_; }
private:
    double* start_;
    int len_;
};

class DoublePointerIterDefaultConstructible: public DoublePointerIter {
    // an alternate version that is default-constructible
public:
    DoublePointerIterDefaultConstructible() :
        DoublePointerIter(0, 0)
    {}
    DoublePointerIterDefaultConstructible(double* start, int len) :
        DoublePointerIter(start, len)
    {}

};
