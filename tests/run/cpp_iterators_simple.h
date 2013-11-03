class DoublePointerIter {
public:
    DoublePointerIter(double* start, int len) : start_(start), len_(len) { }
    double* begin() { return start_; }
    double* end() { return start_ + len_; }
private:
    double* start_;
    int len_;
};

