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
  Integral(long long value) {
    resize_signed_int((unsigned char*)&value, sizeof(value), bytes, N);
  }

  operator long long() const {
    long long value;
    resize_signed_int(bytes, N, (unsigned char*)&value, sizeof(value));
    return value;
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
  
  bool operator==(const long long value) const {
    size_t len = sizeof(long long) > N ? sizeof(long long) : N;
    unsigned char* extended = new unsigned char[len];
    unsigned char* other;
    if (sizeof(long long) < N) {
        resize_signed_int((unsigned char*)&value, sizeof(value), extended, len);
        other = bytes;
    } else {
        resize_signed_int(bytes, N, extended, len);
    }
    bool res = memcmp(extended, other, len);
    delete extended;
    return res;
  }
  bool operator!=(const long long val) const
  { return !(*this == val); }

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
  
  static void resize_signed_int(const unsigned char* src, size_t src_len, unsigned char* dst, size_t dst_len) {
    unsigned char msb;
    size_t dst_offset = 0;
    size_t src_offset = 0;
    if (is_le()) {
        dst_offset = 0;
        src_offset = 0;
        msb = ((unsigned char*) src)[src_len - 1];
        if (src_len > dst_len) {
            src_len = dst_len;
        }
    } else {
        if (dst_len > src_len) {
            dst_offset = dst_len - src_len;
        } else {
            src_offset = src_len - dst_len;
            src_len = dst_len;
        }
        msb = ((unsigned char*) src)[0];
    }
    if (msb & 0x80) {
        memset(dst, 0xFF, dst_len);
    } else {
        memset(dst, 0, dst_len);
    }
    memcpy(dst + dst_offset, src + src_offset, src_len);
  }
};

typedef Integral<3> Int24;
typedef Integral<7> Int56;
typedef Integral<11> Int88;
typedef Integral<64> Int512;
