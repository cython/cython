// -*- c++ -*-
#include <stdio.h>
template<unsigned int N>
class Integral {

  unsigned char bytes[N];

 public:
  Integral() {
    for (unsigned int i=0; i<N; i++)
      bytes[i] = 0;
  }
  Integral(const Integral &I) {
    for (unsigned int i=0; i<N; i++)
      bytes[i] = I.bytes[i];
  }
  Integral(signed char I) {
    unsigned char p = (I<0) ? 0xFF : 0x00;
    for (unsigned int i=0; i<N; i++)
      bytes[i] = p;
    bytes[lsb()] = *(unsigned char*)&I;
  }

  operator signed char() const {
    return *(signed char*)&bytes[lsb()];
  }
  Integral& operator=(const Integral &I) {
    for (unsigned int i=0; i<N; i++)
      bytes[i] = I.bytes[i];
    return *this;
  }
  bool operator<(const Integral &I) const
  { return cmp(I) < 0; }
  bool operator>(const Integral &I) const
  { return cmp(I) > 0; }
  bool operator<=(const Integral &I) const
  { return cmp(I) <= 0; }
  bool operator>=(const Integral &I) const
  { return cmp(I) >= 0; }
  bool operator==(const Integral &I) const
  { return cmp(I) == 0; }
  bool operator!=(const Integral &I) const
  { return cmp(I) != 0; }

 private:
  static bool is_le() {
    int one = 1;
    int b = (int)*(unsigned char *)&one;
    return b ? true : false;
  }
  static unsigned int lsb() {
    return is_le() ? 0 : N-1;
  }
  static unsigned int msb() {
    return is_le() ? N-1 : 0;
  }
  int cmp(const Integral& J) const {
    const Integral& I = *this;
    unsigned char sI = I.bytes[msb()] & 0x80;
    unsigned char sJ = J.bytes[msb()] & 0x80;
    if (sI > sJ) return -1;
    if (sI < sJ) return +1;
    unsigned char bI = I.bytes[msb()] & 0x7F;
    unsigned char bJ = J.bytes[msb()] & 0x7F;
    int cmpabs = 0;
    if (bI < bJ)
      cmpabs = -1;
    else if (bI > bJ)
      cmpabs = +1;
    else {
      int incr = is_le() ? -1 : 1;
      unsigned int i = msb() + incr;
      while (i != lsb()) {
	if (I.bytes[i] < J.bytes[i])
	  { cmpabs = -1;  break; }
	if (I.bytes[i] > J.bytes[i])
	  { cmpabs = +1;  break; }
	i += incr;
      }
    }
    if (sI) return -cmpabs;
    else    return +cmpabs;
  }

};

typedef Integral<3> Int24;
typedef Integral<7> Int56;
typedef Integral<11> Int88;
typedef Integral<64> Int512;
