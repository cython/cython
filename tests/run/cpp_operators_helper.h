#define UN_OP(op) const char* operator op () { return "unary "#op; }
#define POST_UN_OP(op) const char* operator op (int x) { x++; return "post "#op; }
#define BIN_OP(op) const char* operator op (int x) { x++; return "binary "#op; }
#define NONMEMBER_BIN_OP(op) const char* operator op (int x, const TestOps&) { x++; return "nonmember binary "#op; }
#define NONMEMBER_BIN_OP2(op) const char* operator op (double x, const TestOps&) { x++; return "nonmember binary2 "#op; }

#define COMMA ,

class TestOps {

public:

    UN_OP(-);
    UN_OP(+);
    UN_OP(*);
    UN_OP(~);
    UN_OP(!);
    UN_OP(&);

    UN_OP(++);
    UN_OP(--);
    POST_UN_OP(++);
    POST_UN_OP(--);

    BIN_OP(+);
    BIN_OP(-);
    BIN_OP(*);
    BIN_OP(/);
    BIN_OP(%);

    BIN_OP(<<);
    BIN_OP(>>);

    BIN_OP(|);
    BIN_OP(&);
    BIN_OP(^);
    BIN_OP(COMMA);

    BIN_OP(==);
    BIN_OP(!=);
    BIN_OP(<=);
    BIN_OP(<);
    BIN_OP(>=);
    BIN_OP(>);

    BIN_OP([]);
    BIN_OP(());

};

NONMEMBER_BIN_OP(+)
NONMEMBER_BIN_OP(-)
NONMEMBER_BIN_OP(*)
NONMEMBER_BIN_OP(/)
NONMEMBER_BIN_OP(%)

NONMEMBER_BIN_OP(<<)
NONMEMBER_BIN_OP(>>)

NONMEMBER_BIN_OP(|)
NONMEMBER_BIN_OP(&)
NONMEMBER_BIN_OP(^)
NONMEMBER_BIN_OP(COMMA)

NONMEMBER_BIN_OP2(+)
NONMEMBER_BIN_OP2(-)
NONMEMBER_BIN_OP2(*)
NONMEMBER_BIN_OP2(/)
NONMEMBER_BIN_OP2(%)

NONMEMBER_BIN_OP2(<<)
NONMEMBER_BIN_OP2(>>)

NONMEMBER_BIN_OP2(|)
NONMEMBER_BIN_OP2(&)
NONMEMBER_BIN_OP2(^)
NONMEMBER_BIN_OP2(COMMA)

class TruthClass {
public:
  TruthClass() : value(false) {}
  TruthClass(bool value) : value(value) {}
  virtual ~TruthClass() {};
  operator bool() { return value; }
  bool value;
};
