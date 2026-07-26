cdef extern from "Python.h":
    ############################################################################
    # 7.2.3
    ############################################################################
    # PyFloatObject
    #
    # This subtype of PyObject represents a Python floating point object.

    # PyTypeObject PyFloat_Type
    #
    # This instance of PyTypeObject represents the Python floating
    # point type. This is the same object as float and
    # types.FloatType.

    bint PyFloat_Check(object p)
    # Return true if its argument is a PyFloatObject or a subtype of
    # PyFloatObject.

    bint PyFloat_CheckExact(object p)
    # Return true if its argument is a PyFloatObject, but not a
    # subtype of PyFloatObject.

    object PyFloat_FromString(object str)
    # Return value: New reference.
    # Create a PyFloatObject object based on the string value in str,
    # or NULL on failure. The pend argument is ignored. It remains
    # only for backward compatibility.

    object PyFloat_FromDouble(double v)
    # Return value: New reference.
    # Create a PyFloatObject object from v, or NULL on failure.

    double PyFloat_AsDouble(object pyfloat) except? -1
    # Return a C double representation of the contents of pyfloat.

    double PyFloat_AS_DOUBLE(object pyfloat)
    # Return a C double representation of the contents of pyfloat, but
    # without error checking.

    int PyFloat_Pack2(double x, unsigned char *p, int le) except -1
    # Pack a C double as the IEEE 754 binary16 half-precision format.

    int PyFloat_Pack4(double x, unsigned char *p, int le) except -1
    # Pack a C double as the IEEE 754 binary32 single precision format.

    int PyFloat_Pack8(double x, unsigned char *p, int le) except -1
    # Pack a C double as the IEEE 754 binary64 double precision format.

    double PyFloat_Unpack2(const unsigned char *p, int le) except? -1.0
    # Unpack the IEEE 754 binary16 half-precision format as a C double.

    double PyFloat_Unpack4(const unsigned char *p, int le) except? -1.0
    # Unpack the IEEE 754 binary32 single precision format as a C double.

    double PyFloat_Unpack8(const unsigned char *p, int le) except? -1.0
    # Unpack the IEEE 754 binary64 double precision format as a C double.
