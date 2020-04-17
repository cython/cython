///////////////////////// NumpyImportArray.init ////////////////////

// comment below is deliberately kept in the generated C file to
// help users debug where this came from:
/*
 * Cython has automatically inserted a call to _import_array since
 * you didn't include one when your cimported numpy. To disable this
 * add the line
 *   <void>_import_array
 */
#ifdef NPY_NDARRAYOBJECT_H /* numpy headers have been included */
#if !NO_IMPORT_ARRAY /* can be explicitly set to tell Numpy its initialization is done manually */
if (_import_array() == -1) __PYX_ERR(1, 1, __pyx_L1_error) /* __pyx_L1_error reliably exists in __Pyx_InitGlobals */
#endif
#endif
