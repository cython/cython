/////////////// CppExceptionConversion.proto ///////////////

#ifndef __Pyx_CppExn2PyErr
#include <new>
#include <typeinfo>
#include <stdexcept>
#include <ios>

static void __Pyx_CppExn2PyErr() {
  // Catch a handful of different errors here and turn them into the
  // equivalent Python errors.
  try {
    if (PyErr_Occurred())
      ; // let the latest Python exn pass through and ignore the current one
    else
      throw;
  } catch (const std::bad_alloc& exn) {
    PyErr_SetString(PyExc_MemoryError, exn.what());
  } catch (const std::bad_cast& exn) {
    PyErr_SetString(PyExc_TypeError, exn.what());
  } catch (const std::bad_typeid& exn) {
    PyErr_SetString(PyExc_TypeError, exn.what());
  } catch (const std::domain_error& exn) {
    PyErr_SetString(PyExc_ValueError, exn.what());
  } catch (const std::invalid_argument& exn) {
    PyErr_SetString(PyExc_ValueError, exn.what());
  } catch (const std::ios_base::failure& exn) {
    // Unfortunately, in standard C++ we have no way of distinguishing EOF
    // from other errors here; be careful with the exception mask
    PyErr_SetString(PyExc_IOError, exn.what());
  } catch (const std::out_of_range& exn) {
    // Change out_of_range to IndexError
    PyErr_SetString(PyExc_IndexError, exn.what());
  } catch (const std::overflow_error& exn) {
    PyErr_SetString(PyExc_OverflowError, exn.what());
  } catch (const std::range_error& exn) {
    PyErr_SetString(PyExc_ArithmeticError, exn.what());
  } catch (const std::underflow_error& exn) {
    PyErr_SetString(PyExc_ArithmeticError, exn.what());
  } catch (const std::exception& exn) {
    PyErr_SetString(PyExc_RuntimeError, exn.what());
  }
  catch (...)
  {
    PyErr_SetString(PyExc_RuntimeError, "Unknown exception");
  }
}
#endif

/////////////// PythranConversion.proto ///////////////

template <class T>
auto __Pyx_pythran_to_python(T &&value) -> decltype(to_python(
      typename pythonic::returnable<typename std::remove_cv<typename std::remove_reference<T>::type>::type>::type{std::forward<T>(value)}))
{
  using returnable_type = typename pythonic::returnable<typename std::remove_cv<typename std::remove_reference<T>::type>::type>::type;
  return to_python(returnable_type{std::forward<T>(value)});
}

#define __Pyx_PythranShapeAccessor(x) (pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x))

////////////// MoveIfSupported.proto //////////////////

#if __cplusplus >= 201103L || (defined(_MSC_VER) && _MSC_VER >= 1600)
  // move should be defined for these versions of MSVC, but __cplusplus isn't set usefully
  #include <utility>
  #define __PYX_STD_MOVE_IF_SUPPORTED(x) std::move(x)
#else
  #define __PYX_STD_MOVE_IF_SUPPORTED(x) x
#endif

////////////// EnumClassDecl.proto //////////////////

#if defined (_MSC_VER)
  #if PY_VERSION_HEX >= 0x03040000 && PY_VERSION_HEX < 0x03050000
    #define __PYX_ENUM_CLASS_DECL
  #else
    #define __PYX_ENUM_CLASS_DECL enum
  #endif
#else
  #define __PYX_ENUM_CLASS_DECL enum
#endif
