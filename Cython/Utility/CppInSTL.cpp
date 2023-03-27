//////////////////// InContainers.proto ////////////////////

#include <algorithm>

namespace __operator_in_containers_helpers__ {

template<class Container, class T>
class has_find_contains
{
  typedef char yes[1];
  typedef char no[2];

  template<class U, U>
  struct TypeCheck
  {};

  template<class C> static yes& _has_find(TypeCheck<typename C::const_iterator (C::*)(const T&) const, &C::find> *);
  template<class C> static no&  _has_find(...);

  template<class C> static yes& _has_contains(TypeCheck<bool (C::*)(const T&) const, &C::contains> *);
  template<class C> static no&  _has_contains(...);

public:
  enum { has_contains = sizeof(_has_contains<Container>(0)) == sizeof(yes) };
  enum { has_find = sizeof(_has_find<Container>(0)) == sizeof(yes) };
};

template<class Container, class T, bool has_contains, bool has_find>
struct InContainer
{};

template<class Container, class T>
struct InContainer<Container, T, false, false>
{
  bool
  in(const T& x, const Container& c) const
  {
    return std::find(c.begin(), c.end(), x) != c.end();
  }
};

template<class Container, class T>
struct InContainer<Container, T, false, true>
{
  typedef void has_find;

  bool
  in(const T& x, const Container& c) const
  {
    return c.find(x) != c.end();
  }
};

template<class Container, class T, bool has_find>
struct InContainer<Container, T, true, has_find>
{
  typedef void has_contains;

  bool
  in(const T& x, const Container& c) const
  {
    return c.contains(x);
  }
};

template<class Container, class T>
bool is_in(const T& x, const Container& c)
{
  return InContainer<Container, T,
                     has_find_contains<Container, T>::has_contains,
                     has_find_contains<Container, T>::has_find>().in(x, c);
}

}
