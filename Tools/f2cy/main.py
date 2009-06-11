import os, sys
from fparser import api
from fparser import block_statements
from Visitor import PrintTree, KindResolutionVisitor, AutoConfigGenerator

def ckind_from_fkind(basic_type, kind):
    #XXX this makes many assumptions -- rewrite for general compiler!!!
    int_map = {
            1: 'c_signed_char',
            2: 'c_short',
            4: 'c_int',
            8: 'c_long'
            }
    real_map = {
            4: 'c_float',
            8: 'c_double',
            10: 'c_long_double', #??? Why 10?
            }
    complex_map = {
            4: 'c_float_complex',
            8: 'c_long_complex',
            10: 'c_long_double_complex',
            }
    logical_map = {
            1: 'c_bool',
            }
    character_map = {
            1: 'c_char'
            }
    map_dispatch = {
            'integer': int_map,
            'real'   : real_map,
            'complex': complex_map,
            'logical': logical_map,
            'character': character_map
            }
    try: int_kind = int(kind)
    except ValueError: return 'c_long' # FIXME: not for general usage!!!
    return map_dispatch[basic_type][int(kind)]

def wrap_subprogram(subp_tree, output_dir, orig_filename):
    '''
    Generates wrapping for a subprogram.

    Hacky proof of concept -- prototype only!

    subp_tree -- parse tree of subroutine | function to wrap.
    '''
    assert isinstance(subp_tree, (block_statements.Function, block_statements.Subroutine))
    # only works for subroutine for now...
    if isinstance(subp_tree, block_statements.Function): return
    wrap_filename = "wrap_%s" % orig_filename
    wrap_path = os.path.join(output_dir, wrap_filename)
    wrap_fh = open(wrap_path, 'a')
    wrap_fh.write('\n')
    # write the declaration
    wrap_subp_name = "wrap_%s" % subp_tree.name
    subp_args_list = "(%s)" % ", ".join(subp_tree.args)
    bind_clause = 'bind(c,name="%s")' % subp_tree.name
    if isinstance(subp_tree, block_statements.Subroutine):
        subp_type = "subroutine"
    elif isinstance(subp_tree, block_statements.Function):
        subp_type = "function"
    else:
        assert False
    wrap_fh.write(" ".join([subp_type, wrap_subp_name, subp_args_list, bind_clause]))
    wrap_fh.write('\n')
    wrap_fh.write("implicit none\n")
    # specifiers for the dummy args
    for arg in subp_tree.args:
        var = subp_tree.a.variables[arg]
        ckind = ckind_from_fkind(var.typedecl.name, var.typedecl.selector[1])
        wrap_fh.write("%s(kind=%s), intent(%s) :: %s\n" % (var.typedecl.name,
            ckind, var.intent[0], var.name))
    # spec for return variable here if function...
    wrap_fh.write('\n')
    # interface for wrapped subprogram...
    # call subprogram -- small difference for function here...
    wrap_fh.write("call %s(%s)\n" % (subp_tree.name, subp_args_list))
    wrap_fh.write('\n')
    # write end statement
    wrap_fh.write("end %s %s\n" % (subp_type, wrap_subp_name))
    wrap_fh.write('\n')
    wrap_fh.close()


def wrap(filename, directory, workdir):
    print >>sys.stderr, "wrapping %s from %s in %s" % (filename, directory, workdir)
    block = api.parse(os.path.join(directory, filename), analyze=True)
    KindResolutionVisitor()(block)
    AutoConfigGenerator()(block, open('%s_autoconf.f95'%filename.split('.')[0],'w'))

