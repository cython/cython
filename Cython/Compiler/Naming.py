#
#   Pyrex - C naming conventions
#
#
#   Prefixes for generating C names.
#   Collected here to facilitate ensuring uniqueness.
#

pyrex_prefix    = "__pyx_"

builtin_prefix    = pyrex_prefix + "builtin_"
arg_prefix        = pyrex_prefix + "arg_"
funcdoc_prefix    = pyrex_prefix + "doc_"
enum_prefix       = pyrex_prefix + "e_"
func_prefix       = pyrex_prefix + "f_"
pyfunc_prefix     = pyrex_prefix + "pf_"
gstab_prefix      = pyrex_prefix + "getsets_"
prop_get_prefix   = pyrex_prefix + "getprop_"
const_prefix      = pyrex_prefix + "k"
label_prefix      = pyrex_prefix + "L"
pymethdef_prefix  = pyrex_prefix + "mdef_"
methtab_prefix    = pyrex_prefix + "methods_"
memtab_prefix     = pyrex_prefix + "members_"
interned_prefix   = pyrex_prefix + "n_"
interned_num_prefix = pyrex_prefix + "int_"
objstruct_prefix  = pyrex_prefix + "obj_"
typeptr_prefix    = pyrex_prefix + "ptype_"
prop_set_prefix   = pyrex_prefix + "setprop_"
type_prefix       = pyrex_prefix + "t_"
typeobj_prefix    = pyrex_prefix + "type_"
var_prefix        = pyrex_prefix + "v_"
vtable_prefix     = pyrex_prefix + "vtable_"
vtabptr_prefix    = pyrex_prefix + "vtabptr_"
vtabstruct_prefix = pyrex_prefix + "vtabstruct_"
opt_arg_prefix    = pyrex_prefix + "opt_args_"

args_cname       = pyrex_prefix + "args"
kwdlist_cname    = pyrex_prefix + "argnames"
obj_base_cname   = pyrex_prefix + "base"
builtins_cname   = pyrex_prefix + "b"
preimport_cname  = pyrex_prefix + "i"
moddict_cname    = pyrex_prefix + "d"
dummy_cname      = pyrex_prefix + "dummy"
filename_cname   = pyrex_prefix + "filename"
filetable_cname  = pyrex_prefix + "f"
filenames_cname  = pyrex_prefix + "filenames"
fileinit_cname   = pyrex_prefix + "init_filenames"
intern_tab_cname = pyrex_prefix + "intern_tab"
kwds_cname       = pyrex_prefix + "kwds"
lineno_cname     = pyrex_prefix + "lineno"
clineno_cname    = pyrex_prefix + "clineno"
cfilenm_cname    = pyrex_prefix + "cfilenm"
module_cname     = pyrex_prefix + "m"
moddoc_cname     = pyrex_prefix + "mdoc"
methtable_cname  = pyrex_prefix + "methods"
retval_cname     = pyrex_prefix + "r"
reqd_kwds_cname  = pyrex_prefix + "reqd_kwds"
self_cname       = pyrex_prefix + "self"
stringtab_cname  = pyrex_prefix + "string_tab"
vtabslot_cname   = pyrex_prefix + "vtab"
c_api_tab_cname  = pyrex_prefix + "c_api_tab"
gilstate_cname   = pyrex_prefix + "state"
skip_dispatch_cname = pyrex_prefix + "skip_dispatch"
empty_tuple      = pyrex_prefix + "empty_tuple"
cleanup_cname    = pyrex_prefix + "module_cleanup"
optional_args_cname = pyrex_prefix + "optional_args"
no_opt_args      = pyrex_prefix + "no_opt_args"

line_c_macro = "__LINE__"

file_c_macro = "__FILE__"

extern_c_macro  = pyrex_prefix.upper() + "EXTERN_C"

exc_type_name   = pyrex_prefix + "exc_type"
exc_value_name  = pyrex_prefix + "exc_value"
exc_tb_name     = pyrex_prefix + "exc_tb"
exc_lineno_name = pyrex_prefix + "exc_lineno"

exc_vars = (exc_type_name, exc_value_name, exc_tb_name)

api_name        = pyrex_prefix + "capi__"

h_guard_prefix   = "__PYX_HAVE__"
api_guard_prefix = "__PYX_HAVE_API__"
api_func_guard   = "__PYX_HAVE_API_FUNC_"

def py_version_hex(major, minor=0, micro=0, release_level=0, release_serial=0):
    return (major << 24) | (minor << 16) | (micro << 8) | (release_level << 4) | (release_serial)
