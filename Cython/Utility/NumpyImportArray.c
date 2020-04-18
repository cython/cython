///////////////////////// NumpyImportArray.init ////////////////////

// comment below is deliberately kept in the generated C file to
// help users debug where this came from:
/*
 * Cython has automatically inserted a call to _import_array since
 * you didn't include one when you cimported numpy. To disable this
 * add the line
 *   <void>_import_array
 */
#ifdef NPY_NDARRAYOBJECT_H /* numpy headers have been included */
// NO_IMPORT_ARRAY is Numpy's mechanism for indicating that import_array is handled elsewhere
#if !NO_IMPORT_ARRAY /* https://docs.scipy.org/doc/numpy-1.17.0/reference/c-api.array.html#c.NO_IMPORT_ARRAY  */
if (unlikely(_import_array() == -1)) {
    PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import");
    {{ err_goto }};
}
#endif
#endif
