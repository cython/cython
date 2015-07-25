#define UN_OP(op) const char* operator op () { return "unary "#op; }
#define POST_UN_OP(op) const char* operator op (int x) { x++; return "post "#op; }
#define BIN_OP(op) const char* operator op (int x) { x++; return "binary "#op; }

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

class TruthClass {
public:
  TruthClass() : value(false) {}
  TruthClass(bool value) : value(value) {}
  operator bool() { return value; }
  bool value;
};
