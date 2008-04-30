#
#   Pyrex Parser
#

import os, re
from string import join, replace
from types import ListType, TupleType
from Scanning import PyrexScanner
import Nodes
import ExprNodes
from ModuleNode import ModuleNode
from Errors import error, InternalError
from Cython import Utils

def p_ident(s, message = "Expected an identifier"):
    if s.sy == 'IDENT':
        name = s.systring
        s.next()
        return name
    else:
        s.error(message)

def p_ident_list(s):
    names = []
    while s.sy == 'IDENT':
        names.append(s.systring)
        s.next()
        if s.sy != ',':
            break
        s.next()
    return names

#------------------------------------------
#
#   Expressions
#
#------------------------------------------

def p_binop_expr(s, ops, p_sub_expr):
    #print "p_binop_expr:", ops, p_sub_expr ###
    n1 = p_sub_expr(s)
    #print "p_binop_expr(%s):" % p_sub_expr, s.sy ###
    while s.sy in ops:
        op = s.sy
        pos = s.position()
        s.next()
        n2 = p_sub_expr(s)
        n1 = ExprNodes.binop_node(pos, op, n1, n2)
    return n1

#expression: or_test [if or_test else test] | lambda_form

def p_simple_expr(s):
    pos = s.position()
    expr = p_or_test(s)
    if s.sy == 'if':
        s.next()
        test = p_or_test(s)
        if s.sy == 'else':
            s.next()
            other = p_test(s)
            return ExprNodes.CondExprNode(pos, test=test, true_val=expr, false_val=other)
        else:
            s.error("Expected 'else'")
    else:
        return expr
        
#test: or_test | lambda_form
        
def p_test(s):
    return p_or_test(s)

#or_test: and_test ('or' and_test)*

def p_or_test(s):
    #return p_binop_expr(s, ('or',), p_and_test)
    return p_rassoc_binop_expr(s, ('or',), p_and_test)

def p_rassoc_binop_expr(s, ops, p_subexpr):
    n1 = p_subexpr(s)
    if s.sy in ops:
        pos = s.position()
        op = s.sy
        s.next()
        n2 = p_rassoc_binop_expr(s, ops, p_subexpr)
        n1 = ExprNodes.binop_node(pos, op, n1, n2)
    return n1

#and_test: not_test ('and' not_test)*

def p_and_test(s):
    #return p_binop_expr(s, ('and',), p_not_test)
    return p_rassoc_binop_expr(s, ('and',), p_not_test)

#not_test: 'not' not_test | comparison

def p_not_test(s):
    if s.sy == 'not':
        pos = s.position()
        s.next()
        return ExprNodes.NotNode(pos, operand = p_not_test(s))
    else:
        return p_comparison(s)

#comparison: expr (comp_op expr)*
#comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'

def p_comparison(s):
    n1 = p_bit_expr(s)
    if s.sy in comparison_ops:
        pos = s.position()
        op = p_cmp_op(s)
        n2 = p_bit_expr(s)
        n1 = ExprNodes.PrimaryCmpNode(pos, 
            operator = op, operand1 = n1, operand2 = n2)
        if s.sy in comparison_ops:
            n1.cascade = p_cascaded_cmp(s)
    return n1

def p_cascaded_cmp(s):
    pos = s.position()
    op = p_cmp_op(s)
    n2 = p_bit_expr(s)
    result = ExprNodes.CascadedCmpNode(pos, 
        operator = op, operand2 = n2)
    if s.sy in comparison_ops:
        result.cascade = p_cascaded_cmp(s)
    return result

def p_cmp_op(s):
    if s.sy == 'not':
        s.next()
        s.expect('in')
        op = 'not_in'
    elif s.sy == 'is':
        s.next()
        if s.sy == 'not':
            s.next()
            op = 'is_not'
        else:
            op = 'is'
    else:
        op = s.sy
        s.next()
    if op == '<>':
        op = '!='
    return op
    
comparison_ops = (
    '<', '>', '==', '>=', '<=', '<>', '!=', 
    'in', 'is', 'not'
)

#expr: xor_expr ('|' xor_expr)*

def p_bit_expr(s):
    return p_binop_expr(s, ('|',), p_xor_expr)

#xor_expr: and_expr ('^' and_expr)*

def p_xor_expr(s):
    return p_binop_expr(s, ('^',), p_and_expr)

#and_expr: shift_expr ('&' shift_expr)*

def p_and_expr(s):
    return p_binop_expr(s, ('&',), p_shift_expr)

#shift_expr: arith_expr (('<<'|'>>') arith_expr)*

def p_shift_expr(s):
    return p_binop_expr(s, ('<<', '>>'), p_arith_expr)

#arith_expr: term (('+'|'-') term)*

def p_arith_expr(s):
    return p_binop_expr(s, ('+', '-'), p_term)

#term: factor (('*'|'/'|'%') factor)*

def p_term(s):
    return p_binop_expr(s, ('*', '/', '%', '//'), p_factor)

#factor: ('+'|'-'|'~'|'&'|typecast|sizeof) factor | power

def p_factor(s):
    sy = s.sy
    if sy in ('+', '-', '~'):
        op = s.sy
        pos = s.position()
        s.next()
        return ExprNodes.unop_node(pos, op, p_factor(s))
    elif sy == '&':
        pos = s.position()
        s.next()
        arg = p_factor(s)
        return ExprNodes.AmpersandNode(pos, operand = arg)
    elif sy == "<":
        return p_typecast(s)
    elif sy == 'IDENT' and s.systring == "sizeof":
        return p_sizeof(s)
    else:
        return p_power(s)

def p_typecast(s):
    # s.sy == "<"
    pos = s.position()
    s.next()
    base_type = p_c_base_type(s)
    declarator = p_c_declarator(s, empty = 1)
    if s.sy == '?':
        s.next()
        typecheck = 1
    else:
        typecheck = 0
    s.expect(">")
    operand = p_factor(s)
    return ExprNodes.TypecastNode(pos, 
        base_type = base_type, 
        declarator = declarator,
        operand = operand,
        typecheck = typecheck)

def p_sizeof(s):
    # s.sy == ident "sizeof"
    pos = s.position()
    s.next()
    s.expect('(')
    if looking_at_type(s) or looking_at_dotted_name(s):
        base_type = p_c_base_type(s)
        declarator = p_c_declarator(s, empty = 1)
        node = ExprNodes.SizeofTypeNode(pos, 
            base_type = base_type, declarator = declarator)
    else:
        operand = p_simple_expr(s)
        node = ExprNodes.SizeofVarNode(pos, operand = operand)
    s.expect(')')
    return node

#power: atom trailer* ('**' factor)*

def p_power(s):
    n1 = p_atom(s)
    while s.sy in ('(', '[', '.'):
        n1 = p_trailer(s, n1)
    if s.sy == '**':
        pos = s.position()
        s.next()
        n2 = p_factor(s)
        n1 = ExprNodes.binop_node(pos, '**', n1, n2)
    return n1

#trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME

def p_trailer(s, node1):
    pos = s.position()
    if s.sy == '(':
        return p_call(s, node1)
    elif s.sy == '[':
        return p_index(s, node1)
    else: # s.sy == '.'
        s.next()
        name = p_ident(s)
        return ExprNodes.AttributeNode(pos, 
            obj = node1, attribute = name)

# arglist:  argument (',' argument)* [',']
# argument: [test '='] test       # Really [keyword '='] test

def p_call(s, function):
    # s.sy == '('
    pos = s.position()
    s.next()
    positional_args = []
    keyword_args = []
    star_arg = None
    starstar_arg = None
    while s.sy not in ('*', '**', ')'):
        arg = p_simple_expr(s)
        if s.sy == '=':
            s.next()
            if not arg.is_name:
                s.error("Expected an identifier before '='",
                    pos = arg.pos)
            encoded_name = Utils.EncodedString(arg.name)
            encoded_name.encoding = s.source_encoding
            keyword = ExprNodes.StringNode(arg.pos, 
                value = encoded_name)
            arg = p_simple_expr(s)
            keyword_args.append((keyword, arg))
        else:
            if keyword_args:
                s.error("Non-keyword arg following keyword arg",
                    pos = arg.pos)
            positional_args.append(arg)
        if s.sy != ',':
            break
        s.next()
    if s.sy == '*':
        s.next()
        star_arg = p_simple_expr(s)
        if s.sy == ',':
            s.next()
    if s.sy == '**':
        s.next()
        starstar_arg = p_simple_expr(s)
        if s.sy == ',':
            s.next()
    s.expect(')')
    if not (keyword_args or star_arg or starstar_arg):
        return ExprNodes.SimpleCallNode(pos,
            function = function,
            args = positional_args)
    else:
        arg_tuple = None
        keyword_dict = None
        if positional_args or not star_arg:
            arg_tuple = ExprNodes.TupleNode(pos, 
                args = positional_args)
        if star_arg:
            star_arg_tuple = ExprNodes.AsTupleNode(pos, arg = star_arg)
            if arg_tuple:
                arg_tuple = ExprNodes.binop_node(pos, 
                    operator = '+', operand1 = arg_tuple,
                    operand2 = star_arg_tuple)
            else:
                arg_tuple = star_arg_tuple
        if keyword_args:
            keyword_args = [ExprNodes.DictItemNode(pos=key.pos, key=key, value=value) 
                              for key, value in keyword_args]
            keyword_dict = ExprNodes.DictNode(pos,
                key_value_pairs = keyword_args)
        return ExprNodes.GeneralCallNode(pos, 
            function = function,
            positional_args = arg_tuple,
            keyword_args = keyword_dict,
            starstar_arg = starstar_arg)

#lambdef: 'lambda' [varargslist] ':' test

#subscriptlist: subscript (',' subscript)* [',']

def p_index(s, base):
    # s.sy == '['
    pos = s.position()
    s.next()
    subscripts = p_subscript_list(s)
    if len(subscripts) == 1 and len(subscripts[0]) == 2:
        start, stop = subscripts[0]
        result = ExprNodes.SliceIndexNode(pos, 
            base = base, start = start, stop = stop)
    else:
        indexes = make_slice_nodes(pos, subscripts)
        if len(indexes) == 1:
            index = indexes[0]
        else:
            index = ExprNodes.TupleNode(pos, args = indexes)
        result = ExprNodes.IndexNode(pos,
            base = base, index = index)
    s.expect(']')
    return result

def p_subscript_list(s):
    items = [p_subscript(s)]
    while s.sy == ',':
        s.next()
        if s.sy == ']':
            break
        items.append(p_subscript(s))
    return items

#subscript: '.' '.' '.' | test | [test] ':' [test] [':' [test]]

def p_subscript(s):
    # Parse a subscript and return a list of
    # 1, 2 or 3 ExprNodes, depending on how
    # many slice elements were encountered.
    pos = s.position()
    if s.sy == '.':
        expect_ellipsis(s)
        return [ExprNodes.EllipsisNode(pos)]
    else:
        start = p_slice_element(s, (':',))
        if s.sy != ':':
            return [start]
        s.next()
        stop = p_slice_element(s, (':', ',', ']'))
        if s.sy != ':':
            return [start, stop]
        s.next()
        step = p_slice_element(s, (':', ',', ']'))
        return [start, stop, step]

def p_slice_element(s, follow_set):
    # Simple expression which may be missing iff
    # it is followed by something in follow_set.
    if s.sy not in follow_set:
        return p_simple_expr(s)
    else:
        return None

def expect_ellipsis(s):
    s.expect('.')
    s.expect('.')
    s.expect('.')

def make_slice_nodes(pos, subscripts):
    # Convert a list of subscripts as returned
    # by p_subscript_list into a list of ExprNodes,
    # creating SliceNodes for elements with 2 or
    # more components.
    result = []
    for subscript in subscripts:
        if len(subscript) == 1:
            result.append(subscript[0])
        else:
            result.append(make_slice_node(pos, *subscript))
    return result

def make_slice_node(pos, start, stop = None, step = None):
    if not start:
        start = ExprNodes.NoneNode(pos)
    if not stop:
        stop = ExprNodes.NoneNode(pos)
    if not step:
        step = ExprNodes.NoneNode(pos)
    return ExprNodes.SliceNode(pos,
        start = start, stop = stop, step = step)

#atom: '(' [testlist] ')' | '[' [listmaker] ']' | '{' [dictmaker] '}' | '`' testlist '`' | NAME | NUMBER | STRING+

def p_atom(s):
    pos = s.position()
    sy = s.sy
    if sy == '(':
        s.next()
        if s.sy == ')':
            result = ExprNodes.TupleNode(pos, args = [])
        else:
            result = p_expr(s)
        s.expect(')')
        return result
    elif sy == '[':
        return p_list_maker(s)
    elif sy == '{':
        return p_dict_maker(s)
    elif sy == '`':
        return p_backquote_expr(s)
    elif sy == 'INT':
        value = s.systring
        s.next()
        return ExprNodes.IntNode(pos, value = value)
    elif sy == 'LONG':
        value = s.systring
        s.next()
        return ExprNodes.LongNode(pos, value = value)
    elif sy == 'FLOAT':
        value = s.systring
        s.next()
        return ExprNodes.FloatNode(pos, value = value)
    elif sy == 'IMAG':
        value = s.systring[:-1]
        s.next()
        return ExprNodes.ImagNode(pos, value = value)
    elif sy == 'BEGIN_STRING':
        kind, value = p_cat_string_literal(s)
        if kind == 'c':
            return ExprNodes.CharNode(pos, value = value)
        else:
            return ExprNodes.StringNode(pos, value = value)
    elif sy == 'IDENT':
        name = s.systring
        s.next()
        if name == "None":
            return ExprNodes.NoneNode(pos)
        elif name == "True":
            return ExprNodes.BoolNode(pos, value=True)
        elif name == "False":
            return ExprNodes.BoolNode(pos, value=False)
        else:
            return p_name(s, name)
    elif sy == 'NULL':
        s.next()
        return ExprNodes.NullNode(pos)
    else:
        s.error("Expected an identifier or literal")

def p_name(s, name):
    pos = s.position()
    if not s.compile_time_expr:
        try:
            value = s.compile_time_env.lookup_here(name)
        except KeyError:
            pass
        else:
            rep = repr(value)
            if isinstance(value, bool):
                return ExprNodes.BoolNode(pos, value = value)
            elif isinstance(value, int):
                return ExprNodes.IntNode(pos, value = rep)
            elif isinstance(value, long):
                return ExprNodes.LongNode(pos, value = rep)
            elif isinstance(value, float):
                return ExprNodes.FloatNode(pos, value = rep)
            elif isinstance(value, str):
                sval = Utils.EncodedString(rep[1:-1])
                sval.encoding = value.encoding
                return ExprNodes.StringNode(pos, value = sval)
            elif isinstance(value, unicode):
                sval = Utils.EncodedString(rep[2:-1])
                return ExprNodes.StringNode(pos, value = sval)
            else:
                error(pos, "Invalid type for compile-time constant: %s"
                    % value.__class__.__name__)
    return ExprNodes.NameNode(pos, name = name)

def p_cat_string_literal(s):
    # A sequence of one or more adjacent string literals.
    # Returns (kind, value) where kind in ('', 'c', 'r', 'u')
    kind, value = p_string_literal(s)
    if kind != 'c':
        strings = [value]
        while s.sy == 'BEGIN_STRING':
            next_kind, next_value = p_string_literal(s)
            if next_kind == 'c':
                error(s.position(),
                      "Cannot concatenate char literal with another string or char literal")
            elif next_kind == 'u':
                kind = 'u'
            strings.append(next_value)
        value = Utils.EncodedString( u''.join(strings) )
        if kind != 'u':
            value.encoding = s.source_encoding
    return kind, value

def p_opt_string_literal(s):
    if s.sy == 'BEGIN_STRING':
        return p_string_literal(s)
    else:
        return None

def p_string_literal(s):
    # A single string or char literal.
    # Returns (kind, value) where kind in ('', 'c', 'r', 'u')
    # s.sy == 'BEGIN_STRING'
    pos = s.position()
    #is_raw = s.systring[:1].lower() == "r"
    kind = s.systring[:1].lower()
    if kind not in "cru":
        kind = ''
    chars = []
    while 1:
        s.next()
        sy = s.sy
        #print "p_string_literal: sy =", sy, repr(s.systring) ###
        if sy == 'CHARS':
            systr = s.systring
            if len(systr) == 1 and systr in "'\"\n":
                chars.append('\\')
            chars.append(systr)
        elif sy == 'ESCAPE':
            systr = s.systring
            if kind == 'r':
                if systr == '\\\n':
                    chars.append(r'\\\n')
                elif systr == r'\"':
                    chars.append(r'\\\"')
                elif systr == r'\\':
                    chars.append(r'\\\\')
                else:
                    chars.append('\\' + systr)
            else:
                c = systr[1]
                if c in "'\"\\abfnrtv01234567":
                    chars.append(systr)
                elif c == '\n':
                    pass
                elif c in 'ux':
                    if kind == 'u':
                        try:
                            chars.append(
                                systr.encode("ASCII").decode('unicode_escape'))
                        except UnicodeDecodeError:
                            s.error("Invalid unicode escape '%s'" % systr,
                                    pos = pos)
                    elif c == 'x':
                        chars.append('\\x0' + systr[2:])
                    else:
                        chars.append(systr)
                else:
                    chars.append(r'\\' + systr[1:])
        elif sy == 'NEWLINE':
            chars.append(r'\n')
        elif sy == 'END_STRING':
            break
        elif sy == 'EOF':
            s.error("Unclosed string literal", pos = pos)
        else:
            s.error(
                "Unexpected token %r:%r in string literal" %
                    (sy, s.systring))
    s.next()
    value = Utils.EncodedString( u''.join(chars) )
    if kind != 'u':
        value.encoding = s.source_encoding
    #print "p_string_literal: value =", repr(value) ###
    return kind, value

# list_display  	::=  	"[" [listmaker] "]"
# listmaker 	::= 	expression ( list_for | ( "," expression )* [","] )
# list_iter 	::= 	list_for | list_if
# list_for 	::= 	"for" expression_list "in" testlist [list_iter]
# list_if 	::= 	"if" test [list_iter]
        
def p_list_maker(s):
    # s.sy == '['
    pos = s.position()
    s.next()
    if s.sy == ']':
        s.expect(']')
        return ExprNodes.ListNode(pos, args = [])
    expr = p_simple_expr(s)
    if s.sy == 'for':
        loop = p_list_for(s)
        s.expect(']')
        inner_loop = loop
        while not isinstance(inner_loop.body, Nodes.PassStatNode):
            inner_loop = inner_loop.body
            if isinstance(inner_loop, Nodes.IfStatNode):
                 inner_loop = inner_loop.if_clauses[0]
        append = ExprNodes.ListComprehensionAppendNode( pos, expr = expr )
        inner_loop.body = Nodes.ExprStatNode(pos, expr = append)
        return ExprNodes.ListComprehensionNode(pos, loop = loop, append = append)
    else:
        exprs = [expr]
        if s.sy == ',':
            s.next()
            exprs += p_simple_expr_list(s)
        s.expect(']')
        return ExprNodes.ListNode(pos, args = exprs)
        
def p_list_iter(s):
    if s.sy == 'for':
        return p_list_for(s)
    elif s.sy == 'if':
        return p_list_if(s)
    else:
        return Nodes.PassStatNode(s.position())

def p_list_for(s):
    # s.sy == 'for'
    pos = s.position()
    s.next()
    kw = p_for_bounds(s)
    kw['else_clause'] = None
    kw['body'] = p_list_iter(s)
    return Nodes.ForStatNode(pos, **kw)
        
def p_list_if(s):
    # s.sy == 'if'
    pos = s.position()
    s.next()
    test = p_test(s)
    return Nodes.IfStatNode(pos, 
        if_clauses = [Nodes.IfClauseNode(pos, condition = test, body = p_list_iter(s))],
        else_clause = None )
    
#dictmaker: test ':' test (',' test ':' test)* [',']

def p_dict_maker(s):
    # s.sy == '{'
    pos = s.position()
    s.next()
    items = []
    while s.sy != '}':
        items.append(p_dict_item(s))
        if s.sy != ',':
            break
        s.next()
    s.expect('}')
    return ExprNodes.DictNode(pos, key_value_pairs = items)
    
def p_dict_item(s):
    key = p_simple_expr(s)
    s.expect(':')
    value = p_simple_expr(s)
    return ExprNodes.DictItemNode(key.pos, key=key, value=value)

def p_backquote_expr(s):
    # s.sy == '`'
    pos = s.position()
    s.next()
    arg = p_expr(s)
    s.expect('`')
    return ExprNodes.BackquoteNode(pos, arg = arg)

def p_simple_expr_list(s):
    exprs = []
    while s.sy not in expr_terminators:
        exprs.append(p_simple_expr(s))
        if s.sy != ',':
            break
        s.next()
    return exprs

def p_expr(s):
    pos = s.position()
    expr = p_simple_expr(s)
    if s.sy == ',':
        s.next()
        exprs = [expr] + p_simple_expr_list(s)
        return ExprNodes.TupleNode(pos, args = exprs)
    else:
        return expr


#testlist: test (',' test)* [',']
# differs from p_expr only in the fact that it cannot contain conditional expressions

def p_testlist(s):
    pos = s.position()
    expr = p_test(s)
    if s.sy == ',':
        exprs = [expr]
        while s.sy == ',':
            s.next()
            exprs.append(p_test(s))
        return ExprNodes.TupleNode(pos, args = exprs)
    else:
        return expr
        
expr_terminators = (')', ']', '}', ':', '=', 'NEWLINE')

#-------------------------------------------------------
#
#   Statements
#
#-------------------------------------------------------

def p_global_statement(s):
    # assume s.sy == 'global'
    pos = s.position()
    s.next()
    names = p_ident_list(s)
    return Nodes.GlobalNode(pos, names = names)

def p_expression_or_assignment(s):
    expr_list = [p_expr(s)]
    while s.sy == '=':
        s.next()
        expr_list.append(p_expr(s))
    if len(expr_list) == 1:
        if re.match("[+*/\%^\&|-]=", s.sy):
            lhs = expr_list[0]
            if not isinstance(lhs, (ExprNodes.AttributeNode, ExprNodes.IndexNode, ExprNodes.NameNode) ):
                error(lhs.pos, "Illegal operand for inplace operation.")
            operator = s.sy[0]
            s.next()
            rhs = p_expr(s)
            return Nodes.InPlaceAssignmentNode(lhs.pos, operator = operator, lhs = lhs, rhs = rhs)
        expr = expr_list[0]
        if isinstance(expr, ExprNodes.StringNode):
            return Nodes.PassStatNode(expr.pos)
        else:
            return Nodes.ExprStatNode(expr.pos, expr = expr)
    else:
        expr_list_list = []
        flatten_parallel_assignments(expr_list, expr_list_list)
        nodes = []
        for expr_list in expr_list_list:
            lhs_list = expr_list[:-1]
            rhs = expr_list[-1]
            if len(lhs_list) == 1:
                node = Nodes.SingleAssignmentNode(rhs.pos, 
                    lhs = lhs_list[0], rhs = rhs)
            else:
                node = Nodes.CascadedAssignmentNode(rhs.pos,
                    lhs_list = lhs_list, rhs = rhs)
            nodes.append(node)
        if len(nodes) == 1:
            return nodes[0]
        else:
            return Nodes.ParallelAssignmentNode(nodes[0].pos, stats = nodes)

def flatten_parallel_assignments(input, output):
    #  The input is a list of expression nodes, representing 
    #  the LHSs and RHS of one (possibly cascaded) assignment 
    #  statement. If they are all sequence constructors with 
    #  the same number of arguments, rearranges them into a
    #  list of equivalent assignments between the individual 
    #  elements. This transformation is applied recursively.
    size = find_parallel_assignment_size(input)
    if size >= 0:
        for i in range(size):
            new_exprs = [expr.args[i] for expr in input]
            flatten_parallel_assignments(new_exprs, output)
    else:
        output.append(input)

def find_parallel_assignment_size(input):
    #  The input is a list of expression nodes. If 
    #  they are all sequence constructors with the same number
    #  of arguments, return that number, else return -1.
    #  Produces an error message if they are all sequence
    #  constructors but not all the same size.
    for expr in input:
        if not expr.is_sequence_constructor:
            return -1
    rhs = input[-1]
    rhs_size = len(rhs.args)
    for lhs in input[:-1]:
        lhs_size = len(lhs.args)
        if lhs_size != rhs_size:
            error(lhs.pos, "Unpacking sequence of wrong size (expected %d, got %d)"
                % (lhs_size, rhs_size))
            return -1
    return rhs_size

def p_print_statement(s):
    # s.sy == 'print'
    pos = s.position()
    s.next()
    if s.sy == '>>':
        s.error("'print >>' not yet implemented")
    args = []
    ewc = 0
    if s.sy not in ('NEWLINE', 'EOF'):
        args.append(p_simple_expr(s))
        while s.sy == ',':
            s.next()
            if s.sy in ('NEWLINE', 'EOF'):
                ewc = 1
                break
            args.append(p_simple_expr(s))
    return Nodes.PrintStatNode(pos, 
        args = args, ends_with_comma = ewc)

def p_del_statement(s):
    # s.sy == 'del'
    pos = s.position()
    s.next()
    args = p_simple_expr_list(s)
    return Nodes.DelStatNode(pos, args = args)

def p_pass_statement(s, with_newline = 0):
    pos = s.position()
    s.expect('pass')
    if with_newline:
        s.expect_newline("Expected a newline")
    return Nodes.PassStatNode(pos)

def p_break_statement(s):
    # s.sy == 'break'
    pos = s.position()
    s.next()
    return Nodes.BreakStatNode(pos)

def p_continue_statement(s):
    # s.sy == 'continue'
    pos = s.position()
    s.next()
    return Nodes.ContinueStatNode(pos)

def p_return_statement(s):
    # s.sy == 'return'
    pos = s.position()
    s.next()
    if s.sy not in statement_terminators:
        value = p_expr(s)
    else:
        value = None
    return Nodes.ReturnStatNode(pos, value = value)

def p_raise_statement(s):
    # s.sy == 'raise'
    pos = s.position()
    s.next()
    exc_type = None
    exc_value = None
    exc_tb = None
    if s.sy not in statement_terminators:
        exc_type = p_simple_expr(s)
        if s.sy == ',':
            s.next()
            exc_value = p_simple_expr(s)
            if s.sy == ',':
                s.next()
                exc_tb = p_simple_expr(s)
    if exc_type or exc_value or exc_tb:
        return Nodes.RaiseStatNode(pos, 
            exc_type = exc_type,
            exc_value = exc_value,
            exc_tb = exc_tb)
    else:
        return Nodes.ReraiseStatNode(pos)

def p_import_statement(s):
    # s.sy in ('import', 'cimport')
    pos = s.position()
    kind = s.sy
    s.next()
    items = [p_dotted_name(s, as_allowed = 1)]
    while s.sy == ',':
        s.next()
        items.append(p_dotted_name(s, as_allowed = 1))
    stats = []
    for pos, target_name, dotted_name, as_name in items:
        if kind == 'cimport':
            stat = Nodes.CImportStatNode(pos, 
                module_name = dotted_name,
                as_name = as_name)
        else:
            if as_name and "." in dotted_name:
                name_list = ExprNodes.ListNode(pos, args = [
                    ExprNodes.StringNode(pos, value = Utils.EncodedString("*"))])
            else:
                name_list = None
            dotted_name = Utils.EncodedString(dotted_name)
            dotted_name.encoding = s.source_encoding
            stat = Nodes.SingleAssignmentNode(pos,
                lhs = ExprNodes.NameNode(pos, 
                    name = as_name or target_name),
                rhs = ExprNodes.ImportNode(pos, 
                    module_name = ExprNodes.StringNode(pos,
                        value = dotted_name),
                    name_list = name_list))
        stats.append(stat)
    return Nodes.StatListNode(pos, stats = stats)

def p_from_import_statement(s):
    # s.sy == 'from'
    pos = s.position()
    s.next()
    (dotted_name_pos, _, dotted_name, _) = \
        p_dotted_name(s, as_allowed = 0)
    if s.sy in ('import', 'cimport'):
        kind = s.sy
        s.next()
    else:
        s.error("Expected 'import' or 'cimport'")
    if s.sy == '*':
        s.error("'import *' not supported")
    imported_names = [p_imported_name(s)]
    while s.sy == ',':
        s.next()
        imported_names.append(p_imported_name(s))
    if kind == 'cimport':
        for (name_pos, name, as_name) in imported_names:
            local_name = as_name or name
            s.add_type_name(local_name)
        return Nodes.FromCImportStatNode(pos,
            module_name = dotted_name,
            imported_names = imported_names)
    else:
        imported_name_strings = []
        items = []
        for (name_pos, name, as_name) in imported_names:
            encoded_name = Utils.EncodedString(name)
            encoded_name.encoding = s.source_encoding
            imported_name_strings.append(
                ExprNodes.StringNode(name_pos, value = encoded_name))
            items.append(
                (name,
                 ExprNodes.NameNode(name_pos, 
                 	name = as_name or name)))
        import_list = ExprNodes.ListNode(
            imported_names[0][0], args = imported_name_strings)
        dotted_name = Utils.EncodedString(dotted_name)
        dotted_name.encoding = s.source_encoding
        return Nodes.FromImportStatNode(pos,
            module = ExprNodes.ImportNode(dotted_name_pos,
                module_name = ExprNodes.StringNode(dotted_name_pos,
                    value = dotted_name),
                name_list = import_list),
            items = items)

def p_imported_name(s):
    pos = s.position()
    name = p_ident(s)
    as_name = p_as_name(s)
    return (pos, name, as_name)

def p_dotted_name(s, as_allowed):
    pos = s.position()
    target_name = p_ident(s)
    as_name = None
    names = [target_name]
    while s.sy == '.':
        s.next()
        names.append(p_ident(s))
    if as_allowed:
        as_name = p_as_name(s)
    return (pos, target_name, join(names, "."), as_name)

def p_as_name(s):
    if s.sy == 'IDENT' and s.systring == 'as':
        s.next()
        return p_ident(s)
    else:
        return None

def p_assert_statement(s):
    # s.sy == 'assert'
    pos = s.position()
    s.next()
    cond = p_simple_expr(s)
    if s.sy == ',':
        s.next()
        value = p_simple_expr(s)
    else:
        value = None
    return Nodes.AssertStatNode(pos, cond = cond, value = value)

statement_terminators = (';', 'NEWLINE', 'EOF')

def p_if_statement(s):
    # s.sy == 'if'
    pos = s.position()
    s.next()
    if_clauses = [p_if_clause(s)]
    while s.sy == 'elif':
        s.next()
        if_clauses.append(p_if_clause(s))
    else_clause = p_else_clause(s)
    return Nodes.IfStatNode(pos,
        if_clauses = if_clauses, else_clause = else_clause)

def p_if_clause(s):
    pos = s.position()
    test = p_simple_expr(s)
    body = p_suite(s)
    return Nodes.IfClauseNode(pos,
        condition = test, body = body)

def p_else_clause(s):
    if s.sy == 'else':
        s.next()
        return p_suite(s)
    else:
        return None

def p_while_statement(s):
    # s.sy == 'while'
    pos = s.position()
    s.next()
    test = p_simple_expr(s)
    body = p_suite(s)
    else_clause = p_else_clause(s)
    return Nodes.WhileStatNode(pos, 
        condition = test, body = body, 
        else_clause = else_clause)

def p_for_statement(s):
    # s.sy == 'for'
    pos = s.position()
    s.next()
    kw = p_for_bounds(s)
    kw['body'] = p_suite(s)
    kw['else_clause'] = p_else_clause(s)
    return Nodes.ForStatNode(pos, **kw)
            
def p_for_bounds(s):
    target = p_for_target(s)
    if s.sy == 'in':
        s.next()
        iterator = p_for_iterator(s)
        return { 'target': target, 'iterator': iterator }
    elif s.sy == 'from':
        s.next()
        bound1 = p_bit_expr(s)
        rel1 = p_for_from_relation(s)
        name2_pos = s.position()
        name2 = p_ident(s)
        rel2_pos = s.position()
        rel2 = p_for_from_relation(s)
        bound2 = p_bit_expr(s)
        step = p_for_from_step(s)
        if not target.is_name:
            error(target.pos, 
                "Target of for-from statement must be a variable name")
        elif name2 != target.name:
            error(name2_pos,
                "Variable name in for-from range does not match target")
        if rel1[0] != rel2[0]:
            error(rel2_pos,
                "Relation directions in for-from do not match")
        return {'target': target, 
                'bound1': bound1, 
                'relation1': rel1, 
                'relation2': rel2,
                'bound2': bound2,
                'step': step }
    else:
        s.error("Expected 'in' or 'from'")

def p_for_from_relation(s):
    if s.sy in inequality_relations:
        op = s.sy
        s.next()
        return op
    else:
        s.error("Expected one of '<', '<=', '>' '>='")

def p_for_from_step(s):
    if s.sy == 'by':
        s.next()
        step = p_bit_expr(s)
        return step
    else:
        return None

inequality_relations = ('<', '<=', '>', '>=')

def p_for_target(s):
    pos = s.position()
    expr = p_bit_expr(s)
    if s.sy == ',':
        s.next()
        exprs = [expr]
        while s.sy != 'in':
            exprs.append(p_bit_expr(s))
            if s.sy != ',':
                break
            s.next()
        return ExprNodes.TupleNode(pos, args = exprs)
    else:
        return expr

def p_for_iterator(s):
    pos = s.position()
    expr = p_testlist(s)
    return ExprNodes.IteratorNode(pos, sequence = expr)

def p_try_statement(s):
    # s.sy == 'try'
    pos = s.position()
    s.next()
    body = p_suite(s)
    except_clauses = []
    else_clause = None
    if s.sy in ('except', 'else'):
        while s.sy == 'except':
            except_clauses.append(p_except_clause(s))
        if s.sy == 'else':
            s.next()
            else_clause = p_suite(s)
        body = Nodes.TryExceptStatNode(pos,
            body = body, except_clauses = except_clauses,
            else_clause = else_clause)
        if s.sy != 'finally':
            return body
        # try-except-finally is equivalent to nested try-except/try-finally
    if s.sy == 'finally':
        s.next()
        finally_clause = p_suite(s)
        return Nodes.TryFinallyStatNode(pos,
            body = body, finally_clause = finally_clause)
    else:
        s.error("Expected 'except' or 'finally'")

def p_except_clause(s):
    # s.sy == 'except'
    pos = s.position()
    s.next()
    exc_type = None
    exc_value = None
    if s.sy != ':':
        exc_type = p_simple_expr(s)
        if s.sy == ',':
            s.next()
            exc_value = p_simple_expr(s)
    body = p_suite(s)
    return Nodes.ExceptClauseNode(pos,
        pattern = exc_type, target = exc_value, body = body)

def p_include_statement(s, level):
    pos = s.position()
    s.next() # 'include'
    _, include_file_name = p_string_literal(s)
    s.expect_newline("Syntax error in include statement")
    if s.compile_time_eval:
        include_file_path = s.context.find_include_file(include_file_name, pos)
        if include_file_path:
            f = Utils.open_source_file(include_file_path, mode="rU")
            s2 = PyrexScanner(f, include_file_path, s, source_encoding=f.encoding)
            try:
                tree = p_statement_list(s2, level)
            finally:
                f.close()
            return tree
        else:
            return None
    else:
        return Nodes.PassStatNode(pos)

def p_with_statement(s):
    pos = s.position()
    s.next() # 'with'
#	if s.sy == 'IDENT' and s.systring in ('gil', 'nogil'):
    if s.sy == 'IDENT' and s.systring == 'nogil':
        state = s.systring
        s.next()
        body = p_suite(s)
        return Nodes.GILStatNode(pos, state = state, body = body)
    else:
        s.error("Only 'with gil' and 'with nogil' implemented",
                pos = pos)
    
def p_simple_statement(s):
    #print "p_simple_statement:", s.sy, s.systring ###
    if s.sy == 'global':
        node = p_global_statement(s)
    elif s.sy == 'print':
        node = p_print_statement(s)
    elif s.sy == 'del':
        node = p_del_statement(s)
    elif s.sy == 'break':
        node = p_break_statement(s)
    elif s.sy == 'continue':
        node = p_continue_statement(s)
    elif s.sy == 'return':
        node = p_return_statement(s)
    elif s.sy == 'raise':
        node = p_raise_statement(s)
    elif s.sy in ('import', 'cimport'):
        node = p_import_statement(s)
    elif s.sy == 'from':
        node = p_from_import_statement(s)
    elif s.sy == 'assert':
        node = p_assert_statement(s)
    elif s.sy == 'pass':
        node = p_pass_statement(s)
    else:
        node = p_expression_or_assignment(s)
    return node

def p_simple_statement_list(s):
    # Parse a series of simple statements on one line
    # separated by semicolons.
    stat = p_simple_statement(s)
    if s.sy == ';':
        stats = [stat]
        while s.sy == ';':
            #print "p_simple_statement_list: maybe more to follow" ###
            s.next()
            if s.sy in ('NEWLINE', 'EOF'):
                break
            stats.append(p_simple_statement(s))
        stat = Nodes.StatListNode(stats[0].pos, stats = stats)
    s.expect_newline("Syntax error in simple statement list")
    return stat

def p_compile_time_expr(s):
    old = s.compile_time_expr
    s.compile_time_expr = 1
    expr = p_expr(s)
    s.compile_time_expr = old
    return expr

def p_DEF_statement(s):
    pos = s.position()
    denv = s.compile_time_env
    s.next() # 'DEF'
    name = p_ident(s)
    s.expect('=')
    expr = p_compile_time_expr(s)
    value = expr.compile_time_value(denv)
    #print "p_DEF_statement: %s = %r" % (name, value) ###
    denv.declare(name, value)
    s.expect_newline()
    return Nodes.PassStatNode(pos)

def p_IF_statement(s, level, cdef_flag, visibility, api):
    pos = s.position
    saved_eval = s.compile_time_eval
    current_eval = saved_eval
    denv = s.compile_time_env
    result = None
    while 1:
        s.next() # 'IF' or 'ELIF'
        expr = p_compile_time_expr(s)
        s.compile_time_eval = current_eval and bool(expr.compile_time_value(denv))
        body = p_suite(s, level, cdef_flag, visibility, api = api)
        if s.compile_time_eval:
            result = body
            current_eval = 0
        if s.sy != 'ELIF':
            break
    if s.sy == 'ELSE':
        s.next()
        s.compile_time_eval = current_eval
        body = p_suite(s, level, cdef_flag, visibility, api = api)
        if current_eval:
            result = body
    if not result:
        result = Nodes.PassStatNode(pos)
    s.compile_time_eval = saved_eval
    return result

def p_statement(s, level, cdef_flag = 0, visibility = 'private', api = 0):
    if s.sy == 'ctypedef':
        if level not in ('module', 'module_pxd'):
            s.error("ctypedef statement not allowed here")
        if api:
            error(s.position(), "'api' not allowed with 'ctypedef'")
        return p_ctypedef_statement(s, level, visibility, api)
    elif s.sy == 'DEF':
        return p_DEF_statement(s)
    elif s.sy == 'IF':
        return p_IF_statement(s, level, cdef_flag, visibility, api)
    else:
        overridable = 0
        if s.sy == 'cdef':
            cdef_flag = 1
            s.next()
        if s.sy == 'cpdef':
            cdef_flag = 1
            overridable = 1
            s.next()
        if cdef_flag:
            if level not in ('module', 'module_pxd', 'function', 'c_class', 'c_class_pxd'):
                s.error('cdef statement not allowed here')
            s.level = level
            return p_cdef_statement(s, level, visibility = visibility,
                                    api = api, overridable = overridable)
    #    elif s.sy == 'cpdef':
    #        s.next()
    #        return p_c_func_or_var_declaration(s, level, s.position(), visibility = visibility, api = api, overridable = True)
        else:
            if api:
                error(s.pos, "'api' not allowed with this statement")
            elif s.sy == 'def':
                if level not in ('module', 'class', 'c_class', 'property'):
                    s.error('def statement not allowed here')
                s.level = level
                return p_def_statement(s)
            elif s.sy == 'class':
                if level != 'module':
                    s.error("class definition not allowed here")
                return p_class_statement(s)
            elif s.sy == 'include':
                if level not in ('module', 'module_pxd'):
                    s.error("include statement not allowed here")
                return p_include_statement(s, level)
            elif level == 'c_class' and s.sy == 'IDENT' and s.systring == 'property':
                return p_property_decl(s)
            elif s.sy == 'pass' and level != 'property':
                return p_pass_statement(s, with_newline = 1)
            else:
                if level in ('c_class_pxd', 'property'):
                    s.error("Executable statement not allowed here")
                if s.sy == 'if':
                    return p_if_statement(s)
                elif s.sy == 'while':
                    return p_while_statement(s)
                elif s.sy == 'for':
                    return p_for_statement(s)
                elif s.sy == 'try':
                    return p_try_statement(s)
                elif s.sy == 'with':
                    return p_with_statement(s)
                else:
                    return p_simple_statement_list(s)

def p_statement_list(s, level,
        cdef_flag = 0, visibility = 'private', api = 0):
    # Parse a series of statements separated by newlines.
    pos = s.position()
    stats = []
    while s.sy not in ('DEDENT', 'EOF'):
        stats.append(p_statement(s, level,
            cdef_flag = cdef_flag, visibility = visibility, api = api))
    if len(stats) == 1:
        return stats[0]
    else:
        return Nodes.StatListNode(pos, stats = stats)

def p_suite(s, level = 'other', cdef_flag = 0,
        visibility = 'private', with_doc = 0, with_pseudo_doc = 0, api = 0):
    pos = s.position()
    s.expect(':')
    doc = None
    stmts = []
    if s.sy == 'NEWLINE':
        s.next()
        s.expect_indent()
        if with_doc or with_pseudo_doc:
            doc = p_doc_string(s)
        body = p_statement_list(s, 
            level = level,
            cdef_flag = cdef_flag, 
            visibility = visibility,
            api = api)
        s.expect_dedent()
    else:
        if api:
            error(s.pos, "'api' not allowed with this statement")
        if level in ('module', 'class', 'function', 'other'):
            body = p_simple_statement_list(s)
        else:
            body = p_pass_statement(s)
            s.expect_newline("Syntax error in declarations")
    if with_doc:
        return doc, body
    else:
        return body

def p_c_base_type(s, self_flag = 0, nonempty = 0):
    # If self_flag is true, this is the base type for the
    # self argument of a C method of an extension type.
    if s.sy == '(':
        return p_c_complex_base_type(s)
    else:
        return p_c_simple_base_type(s, self_flag, nonempty = nonempty)

def p_calling_convention(s):
    if s.sy == 'IDENT' and s.systring in calling_convention_words:
        result = s.systring
        s.next()
        return result
    else:
        return ""

calling_convention_words = ("__stdcall", "__cdecl")

def p_c_complex_base_type(s):
    # s.sy == '('
    pos = s.position()
    s.next()
    base_type = p_c_base_type(s)
    declarator = p_c_declarator(s, empty = 1)
    s.expect(')')
    return Nodes.CComplexBaseTypeNode(pos, 
        base_type = base_type, declarator = declarator)

def p_c_simple_base_type(s, self_flag, nonempty):
    #print "p_c_simple_base_type: self_flag =", self_flag
    is_basic = 0
    signed = 1
    longness = 0
    module_path = []
    pos = s.position()
    if looking_at_base_type(s):
        #print "p_c_simple_base_type: looking_at_base_type at", s.position()
        is_basic = 1
        signed, longness = p_sign_and_longness(s)
        if s.sy == 'IDENT' and s.systring in basic_c_type_names:
            name = s.systring
            s.next()
        else:
            name = 'int'
    elif s.looking_at_type_name():
        name = s.systring
        s.next()
        if nonempty and s.sy != 'IDENT':
            # Make sure this is not a declaration of a variable or 
            # function with the same name as a type.  
            if s.sy == '(':
                s.next()
                if s.sy == '*' or s.sy == '**':
                    s.put_back('(', '(')
                else:
                    s.put_back('(', '(')
                    s.put_back('IDENT', name)
                    name = None
            elif s.sy not in ('*', '**', '['):
                s.put_back('IDENT', name)
                name = None
    elif looking_at_dotted_name(s):
        #print "p_c_simple_base_type: looking_at_type_name at", s.position()
        name = s.systring
        s.next()
        while s.sy == '.':
            module_path.append(name)
            s.next()
            name = p_ident(s)
    else:
        #print "p_c_simple_base_type: not looking at type at", s.position()
        name = None
    return Nodes.CSimpleBaseTypeNode(pos, 
        name = name, module_path = module_path,
        is_basic_c_type = is_basic, signed = signed,
        longness = longness, is_self_arg = self_flag)

def looking_at_type(s):
    return looking_at_base_type(s) or s.looking_at_type_name()

def looking_at_base_type(s):
    #print "looking_at_base_type?", s.sy, s.systring, s.position()
    return s.sy == 'IDENT' and s.systring in base_type_start_words

def looking_at_dotted_name(s):
    if s.sy == 'IDENT':
        name = s.systring
        s.next()
        result = s.sy == '.'
        s.put_back('IDENT', name)
        return result
    else:
        return 0

basic_c_type_names = ("void", "char", "int", "float", "double", "Py_ssize_t", "bint")

sign_and_longness_words = ("short", "long", "signed", "unsigned")

base_type_start_words = \
    basic_c_type_names + sign_and_longness_words

def p_sign_and_longness(s):
    signed = 1
    longness = 0
    while s.sy == 'IDENT' and s.systring in sign_and_longness_words:
        if s.systring == 'unsigned':
            signed = 0
        elif s.systring == 'signed':
            signed = 2
        elif s.systring == 'short':
            longness = -1
        elif s.systring == 'long':
            longness += 1
        s.next()
    return signed, longness

def p_opt_cname(s):
    literal = p_opt_string_literal(s)
    if literal:
        _, cname = literal
    else:
        cname = None
    return cname

def p_c_declarator(s, empty = 0, is_type = 0, cmethod_flag = 0, assignable = 0,
        nonempty = 0, calling_convention_allowed = 0):
    # If empty is true, the declarator must be empty. If nonempty is true,
    # the declarator must be nonempty. Otherwise we don't care.
    # If cmethod_flag is true, then if this declarator declares
    # a function, it's a C method of an extension type.
    pos = s.position()
    if s.sy == '(':
        s.next()
        if s.sy == ')' or looking_at_type(s):
            base = Nodes.CNameDeclaratorNode(pos, name = "", cname = None)
            result = p_c_func_declarator(s, pos, base, cmethod_flag)
        else:
            result = p_c_declarator(s, empty, is_type, cmethod_flag, nonempty = nonempty,
                calling_convention_allowed = 1)
            s.expect(')')
    else:
        result = p_c_simple_declarator(s, empty, is_type, cmethod_flag, assignable, nonempty)
    if not calling_convention_allowed and result.calling_convention and s.sy != '(':
        error(s.position(), "%s on something that is not a function"
            % result.calling_convention)
    while s.sy in ('[', '('):
        pos = s.position()
        if s.sy == '[':
            result = p_c_array_declarator(s, result)
        else: # sy == '('
            s.next()
            result = p_c_func_declarator(s, pos, result, cmethod_flag)
        cmethod_flag = 0
    return result

def p_c_array_declarator(s, base):
    pos = s.position()
    s.next() # '['
    if s.sy != ']':
        dim = p_expr(s)
    else:
        dim = None
    s.expect(']')
    return Nodes.CArrayDeclaratorNode(pos, base = base, dimension = dim)

def p_c_func_declarator(s, pos, base, cmethod_flag):
    #  Opening paren has already been skipped
    args = p_c_arg_list(s, in_pyfunc = 0, cmethod_flag = cmethod_flag,
        nonempty_declarators = 0)
    ellipsis = p_optional_ellipsis(s)
    s.expect(')')
    nogil = p_nogil(s)
    exc_val, exc_check = p_exception_value_clause(s)
    with_gil = p_with_gil(s)
    return Nodes.CFuncDeclaratorNode(pos, 
        base = base, args = args, has_varargs = ellipsis,
        exception_value = exc_val, exception_check = exc_check,
        nogil = nogil or with_gil, with_gil = with_gil)

def p_c_simple_declarator(s, empty, is_type, cmethod_flag, assignable, nonempty):
    pos = s.position()
    calling_convention = p_calling_convention(s)
    if s.sy == '*':
        s.next()
        base = p_c_declarator(s, empty, is_type, cmethod_flag, assignable, nonempty)
        result = Nodes.CPtrDeclaratorNode(pos, 
            base = base)
    elif s.sy == '**': # scanner returns this as a single token
        s.next()
        base = p_c_declarator(s, empty, is_type, cmethod_flag, assignable, nonempty)
        result = Nodes.CPtrDeclaratorNode(pos,
            base = Nodes.CPtrDeclaratorNode(pos,
                base = base))
    else:
        rhs = None
        if s.sy == 'IDENT':
            name = s.systring
            if is_type:
                s.add_type_name(name)
            if empty:
                error(s.position(), "Declarator should be empty")
            s.next()
            cname = p_opt_cname(s)
            if s.sy == '=' and assignable:
                s.next()
                rhs = p_simple_expr(s)
        else:
            if nonempty:
                error(s.position(), "Empty declarator")
            name = ""
            cname = None
        result = Nodes.CNameDeclaratorNode(pos,
            name = name, cname = cname, rhs = rhs)
    result.calling_convention = calling_convention
    return result

def p_nogil(s):
    if s.sy == 'IDENT' and s.systring == 'nogil':
        s.next()
        return 1
    else:
        return 0

def p_with_gil(s):
    if s.sy == 'with':
        s.next()
        s.expect_keyword('gil')
        return 1
    else:
        return 0

def p_exception_value_clause(s):
    exc_val = None
    exc_check = 0
    if s.sy == 'except':
        s.next()
        if s.sy == '*':
            exc_check = 1
            s.next()
        elif s.sy == '+':
            exc_check = '+'
            s.next()
            if s.sy == 'IDENT':
                name = s.systring
                s.next()
                exc_val = p_name(s, name)
        else:
            if s.sy == '?':
                exc_check = 1
                s.next()
            exc_val = p_simple_expr(s)
    return exc_val, exc_check

c_arg_list_terminators = ('*', '**', '.', ')')

#def p_c_arg_list(s, in_pyfunc, cmethod_flag = 0, nonempty_declarators = 0,
#		kw_only = 0):
#	args = []
#	if s.sy not in c_arg_list_terminators:
#		args.append(p_c_arg_decl(s, in_pyfunc, cmethod_flag,
#			nonempty = nonempty_declarators, kw_only = kw_only))
#		while s.sy == ',':
#			s.next()
#			if s.sy in c_arg_list_terminators:
#				break
#			args.append(p_c_arg_decl(s, in_pyfunc), nonempty = nonempty_declarators,
#				kw_only = kw_only)
#	return args

def p_c_arg_list(s, in_pyfunc, cmethod_flag = 0, nonempty_declarators = 0,
        kw_only = 0):
    #  Comma-separated list of C argument declarations, possibly empty.
    #  May have a trailing comma.
    args = []
    is_self_arg = cmethod_flag
    while s.sy not in c_arg_list_terminators:
        args.append(p_c_arg_decl(s, in_pyfunc, is_self_arg,
            nonempty = nonempty_declarators, kw_only = kw_only))
        if s.sy != ',':
            break
        s.next()
        is_self_arg = 0
    return args

def p_optional_ellipsis(s):
    if s.sy == '.':
        expect_ellipsis(s)
        return 1
    else:
        return 0

def p_c_arg_decl(s, in_pyfunc, cmethod_flag = 0, nonempty = 0, kw_only = 0):
    pos = s.position()
    not_none = 0
    default = None
    base_type = p_c_base_type(s, cmethod_flag, nonempty = nonempty)
    declarator = p_c_declarator(s, nonempty = nonempty)
    if s.sy == 'not':
        s.next()
        if s.sy == 'IDENT' and s.systring == 'None':
            s.next()
        else:
            s.error("Expected 'None'")
        if not in_pyfunc:
            error(pos, "'not None' only allowed in Python functions")
        not_none = 1
    if s.sy == '=':
        s.next()
        if 'pxd' in s.level:
            if s.sy not in ['*', '?']:
                error(pos, "default values cannot be specified in pxd files, use ? or *")
            default = 1
            s.next()
        else:
            default = p_simple_expr(s)
    return Nodes.CArgDeclNode(pos,
        base_type = base_type,
        declarator = declarator,
        not_none = not_none,
        default = default,
        kw_only = kw_only)

def p_api(s):
    if s.sy == 'IDENT' and s.systring == 'api':
        s.next()
        return 1
    else:
        return 0

def p_cdef_statement(s, level, visibility = 'private', api = 0,
                     overridable = False):
    pos = s.position()
    visibility = p_visibility(s, visibility)
    api = api or p_api(s)
    if api:
        if visibility not in ('private', 'public'):
            error(pos, "Cannot combine 'api' with '%s'" % visibility)
    if (visibility == 'extern') and s.sy == 'from':
            return p_cdef_extern_block(s, level, pos)
    elif s.sy == 'import':
        s.next()
        return p_cdef_extern_block(s, level, pos)
    elif s.sy == ':':
        return p_cdef_block(s, level, visibility, api)
    elif s.sy == 'class':
        if level not in ('module', 'module_pxd'):
            error(pos, "Extension type definition not allowed here")
        #if api:
        #    error(pos, "'api' not allowed with extension class")
        return p_c_class_definition(s, level, pos, visibility = visibility, api = api)
    elif s.sy == 'IDENT' and s.systring in struct_union_or_enum:
        if level not in ('module', 'module_pxd'):
            error(pos, "C struct/union/enum definition not allowed here")
        #if visibility == 'public':
        #    error(pos, "Public struct/union/enum definition not implemented")
        #if api:
        #    error(pos, "'api' not allowed with '%s'" % s.systring)
        if s.systring == "enum":
            return p_c_enum_definition(s, pos, level, visibility)
        else:
            return p_c_struct_or_union_definition(s, pos, level, visibility)
    elif s.sy == 'pass':
        node = p_pass_statement(s)
        s.expect_newline('Expected a newline')
        return node
    else:
        return p_c_func_or_var_declaration(s, level, pos, visibility, api,
                                           overridable)

def p_cdef_block(s, level, visibility, api):
    return p_suite(s, level, cdef_flag = 1, visibility = visibility, api = api)

def p_cdef_extern_block(s, level, pos):
    include_file = None
    s.expect('from')
    if s.sy == '*':
        s.next()
    else:
        _, include_file = p_string_literal(s)
    body = p_suite(s, level, cdef_flag = 1, visibility = 'extern')
    return Nodes.CDefExternNode(pos,
        include_file = include_file,
        body = body)

struct_union_or_enum = (
    "struct", "union", "enum"
)

def p_c_enum_definition(s, pos, level, visibility, typedef_flag = 0):
    # s.sy == ident 'enum'
    s.next()
    if s.sy == 'IDENT':
        name = s.systring
        s.next()
        s.add_type_name(name)
        cname = p_opt_cname(s)
    else:
        name = None
        cname = None
    items = None
    s.expect(':')
    items = []
    if s.sy != 'NEWLINE':
        p_c_enum_line(s, items)
    else:
        s.next() # 'NEWLINE'
        s.expect_indent()
        while s.sy not in ('DEDENT', 'EOF'):
            p_c_enum_line(s, items)
        s.expect_dedent()
    return Nodes.CEnumDefNode(pos, name = name, cname = cname,
        items = items, typedef_flag = typedef_flag, visibility = visibility,
        in_pxd = level == 'module_pxd')

def p_c_enum_line(s, items):
    if s.sy != 'pass':
        p_c_enum_item(s, items)
        while s.sy == ',':
            s.next()
            if s.sy in ('NEWLINE', 'EOF'):
                break
            p_c_enum_item(s, items)
    else:
        s.next()
    s.expect_newline("Syntax error in enum item list")

def p_c_enum_item(s, items):
    pos = s.position()
    name = p_ident(s)
    cname = p_opt_cname(s)
    value = None
    if s.sy == '=':
        s.next()
        value = p_simple_expr(s)
    items.append(Nodes.CEnumDefItemNode(pos, 
        name = name, cname = cname, value = value))

def p_c_struct_or_union_definition(s, pos, level, visibility, typedef_flag = 0):
    # s.sy == ident 'struct' or 'union'
    kind = s.systring
    s.next()
    name = p_ident(s)
    cname = p_opt_cname(s)
    s.add_type_name(name)
    attributes = None
    if s.sy == ':':
        s.next()
        s.expect('NEWLINE')
        s.expect_indent()
        attributes = []
        while s.sy != 'DEDENT':
            if s.sy != 'pass':
                attributes.append(
                    p_c_func_or_var_declaration(s, level = 'other', pos = s.position()))
            else:
                s.next()
                s.expect_newline("Expected a newline")
        s.expect_dedent()
    else:
        s.expect_newline("Syntax error in struct or union definition")
    return Nodes.CStructOrUnionDefNode(pos, 
        name = name, cname = cname, kind = kind, attributes = attributes,
        typedef_flag = typedef_flag, visibility = visibility,
        in_pxd = level == 'module_pxd')

def p_visibility(s, prev_visibility):
    pos = s.position()
    visibility = prev_visibility
    if s.sy == 'IDENT' and s.systring in ('extern', 'public', 'readonly'):
        visibility = s.systring
        if prev_visibility != 'private' and visibility != prev_visibility:
            s.error("Conflicting visibility options '%s' and '%s'"
                % (prev_visibility, visibility))
        s.next()
    return visibility
    
def p_c_modifiers(s):
    if s.sy == 'IDENT' and s.systring in ('inline',):
        modifier = s.systring
        s.next()
        return [modifier] + p_c_modifiers(s)
    return []

def p_c_func_or_var_declaration(s, level, pos, visibility = 'private', api = 0,
                                overridable = False):
    cmethod_flag = level in ('c_class', 'c_class_pxd')
    modifiers = p_c_modifiers(s)
    base_type = p_c_base_type(s, nonempty = 1)
    declarator = p_c_declarator(s, cmethod_flag = cmethod_flag, assignable = 1, nonempty = 1)
    declarator.overridable = overridable
    if s.sy == ':':
        if level not in ('module', 'c_class'):
            s.error("C function definition not allowed here")
        doc, suite = p_suite(s, 'function', with_doc = 1)
        result = Nodes.CFuncDefNode(pos,
            visibility = visibility,
            base_type = base_type,
            declarator = declarator, 
            body = suite,
            doc = doc,
            modifiers = modifiers,
            api = api,
            overridable = overridable)
    else:
        #if api:
        #    error(s.pos, "'api' not allowed with variable declaration")
        declarators = [declarator]
        while s.sy == ',':
            s.next()
            if s.sy == 'NEWLINE':
                break
            declarator = p_c_declarator(s, cmethod_flag = cmethod_flag, assignable = 1, nonempty = 1)
            declarators.append(declarator)
        s.expect_newline("Syntax error in C variable declaration")
        result = Nodes.CVarDefNode(pos, 
            visibility = visibility,
            base_type = base_type, 
            declarators = declarators,
            in_pxd = level == 'module_pxd',
            api = api,
            overridable = overridable)
    return result

def p_ctypedef_statement(s, level, visibility = 'private', api = 0):
    # s.sy == 'ctypedef'
    pos = s.position()
    s.next()
    visibility = p_visibility(s, visibility)
    if s.sy == 'class':
        return p_c_class_definition(s, level, pos,
            visibility = visibility, typedef_flag = 1, api = api)
    elif s.sy == 'IDENT' and s.systring in ('struct', 'union', 'enum'):
        if s.systring == 'enum':
            return p_c_enum_definition(s, pos, level, visibility, typedef_flag = 1)
        else:
            return p_c_struct_or_union_definition(s, pos, level, visibility,
                typedef_flag = 1)
    else:
        base_type = p_c_base_type(s, nonempty = 1)
        declarator = p_c_declarator(s, is_type = 1, nonempty = 1)
        s.expect_newline("Syntax error in ctypedef statement")
        return Nodes.CTypeDefNode(pos,
            base_type = base_type, declarator = declarator, visibility = visibility,
            in_pxd = level == 'module_pxd')

def p_def_statement(s):
    # s.sy == 'def'
    pos = s.position()
    s.next()
    name = p_ident(s)
    #args = []
    s.expect('(');
    args = p_c_arg_list(s, in_pyfunc = 1, nonempty_declarators = 1)
    star_arg = None
    starstar_arg = None
    if s.sy == '*':
        s.next()
        if s.sy == 'IDENT':
            star_arg = p_py_arg_decl(s)
        if s.sy == ',':
            s.next()
            args.extend(p_c_arg_list(s, in_pyfunc = 1,
                nonempty_declarators = 1, kw_only = 1))
        elif s.sy != ')':
            s.error("Syntax error in Python function argument list")
    if s.sy == '**':
        s.next()
        starstar_arg = p_py_arg_decl(s)
    s.expect(')')
    if p_nogil(s):
        error(s.pos, "Python function cannot be declared nogil")
    doc, body = p_suite(s, 'function', with_doc = 1)
    return Nodes.DefNode(pos, name = name, args = args, 
        star_arg = star_arg, starstar_arg = starstar_arg,
        doc = doc, body = body)

def p_py_arg_decl(s):
    pos = s.position()
    name = p_ident(s)
    return Nodes.PyArgDeclNode(pos, name = name)

def p_class_statement(s):
    # s.sy == 'class'
    pos = s.position()
    s.next()
    class_name = Utils.EncodedString( p_ident(s) )
    class_name.encoding = s.source_encoding
    if s.sy == '(':
        s.next()
        base_list = p_simple_expr_list(s)
        s.expect(')')
    else:
        base_list = []
    doc, body = p_suite(s, 'class', with_doc = 1)
    return Nodes.PyClassDefNode(pos,
        name = class_name,
        bases = ExprNodes.TupleNode(pos, args = base_list),
        doc = doc, body = body)

def p_c_class_definition(s, level, pos, 
        visibility = 'private', typedef_flag = 0, api = 0):
    # s.sy == 'class'
    s.next()
    module_path = []
    class_name = p_ident(s)
    while s.sy == '.':
        s.next()
        module_path.append(class_name)
        class_name = p_ident(s)
    if module_path and visibility != 'extern':
        error(pos, "Qualified class name only allowed for 'extern' C class")
    if module_path and s.sy == 'IDENT' and s.systring == 'as':
        s.next()
        as_name = p_ident(s)
    else:
        as_name = class_name
    s.add_type_name(as_name)
    objstruct_name = None
    typeobj_name = None
    base_class_module = None
    base_class_name = None
    if s.sy == '(':
        s.next()
        base_class_path = [p_ident(s)]
        while s.sy == '.':
            s.next()
            base_class_path.append(p_ident(s))
        if s.sy == ',':
            s.error("C class may only have one base class")
        s.expect(')')
        base_class_module = ".".join(base_class_path[:-1])
        base_class_name = base_class_path[-1]
    if s.sy == '[':
        if visibility not in ('public', 'extern'):
            error(s.position(), "Name options only allowed for 'public' or 'extern' C class")
        objstruct_name, typeobj_name = p_c_class_options(s)
    if s.sy == ':':
        if level == 'module_pxd':
            body_level = 'c_class_pxd'
        else:
            body_level = 'c_class'
        doc, body = p_suite(s, body_level, with_doc = 1)
    else:
        s.expect_newline("Syntax error in C class definition")
        doc = None
        body = None
    if visibility == 'extern':
        if not module_path:
            error(pos, "Module name required for 'extern' C class")
        if typeobj_name:
            error(pos, "Type object name specification not allowed for 'extern' C class")
    elif visibility == 'public':
        if not objstruct_name:
            error(pos, "Object struct name specification required for 'public' C class")
        if not typeobj_name:
            error(pos, "Type object name specification required for 'public' C class")
    elif visibility == 'private':
        if api:
            error(pos, "Only 'public' C class can be declared 'api'")
    else:
        error(pos, "Invalid class visibility '%s'" % visibility)
    return Nodes.CClassDefNode(pos,
        visibility = visibility,
        typedef_flag = typedef_flag,
        api = api,
        module_name = ".".join(module_path),
        class_name = class_name,
        as_name = as_name,
        base_class_module = base_class_module,
        base_class_name = base_class_name,
        objstruct_name = objstruct_name,
        typeobj_name = typeobj_name,
        in_pxd = level == 'module_pxd',
        doc = doc,
        body = body)

def p_c_class_options(s):
    objstruct_name = None
    typeobj_name = None
    s.expect('[')
    while 1:
        if s.sy != 'IDENT':
            break
        if s.systring == 'object':
            s.next()
            objstruct_name = p_ident(s)
        elif s.systring == 'type':
            s.next()
            typeobj_name = p_ident(s)
        if s.sy != ',':
            break
        s.next()
    s.expect(']', "Expected 'object' or 'type'")
    return objstruct_name, typeobj_name

def p_property_decl(s):
    pos = s.position()
    s.next() # 'property'
    name = p_ident(s)
    doc, body = p_suite(s, 'property', with_doc = 1)
    return Nodes.PropertyNode(pos, name = name, doc = doc, body = body)

def p_doc_string(s):
    if s.sy == 'BEGIN_STRING':
        _, result = p_cat_string_literal(s)
        if s.sy != 'EOF':
            s.expect_newline("Syntax error in doc string")
        return result
    else:
        return None

def p_module(s, pxd, full_module_name):
    s.add_type_name("object")
    pos = s.position()
    doc = p_doc_string(s)
    if pxd:
        level = 'module_pxd'
    else:
        level = 'module'
    body = p_statement_list(s, level)
    if s.sy != 'EOF':
        s.error("Syntax error in statement [%s,%s]" % (
            repr(s.sy), repr(s.systring)))
    return ModuleNode(pos, doc = doc, body = body, full_module_name = full_module_name)

#----------------------------------------------
#
#   Debugging
#
#----------------------------------------------

def print_parse_tree(f, node, level, key = None):	
    from Nodes import Node
    ind = "  " * level
    if node:
        f.write(ind)
        if key:
            f.write("%s: " % key)
        t = type(node)
        if t == TupleType:
            f.write("(%s @ %s\n" % (node[0], node[1]))
            for i in xrange(2, len(node)):
                print_parse_tree(f, node[i], level+1)
            f.write("%s)\n" % ind)
            return
        elif isinstance(node, Node):
            try:
                tag = node.tag
            except AttributeError:
                tag = node.__class__.__name__
            f.write("%s @ %s\n" % (tag, node.pos))
            for name, value in node.__dict__.items():
                if name != 'tag' and name != 'pos':
                    print_parse_tree(f, value, level+1, name)
            return
        elif t == ListType:
            f.write("[\n")
            for i in xrange(len(node)):
                print_parse_tree(f, node[i], level+1)
            f.write("%s]\n" % ind)
            return
    f.write("%s%s\n" % (ind, node))

