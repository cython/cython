# cython: auto_cpdef=True
#
#   Pyrex Parser
#

# This should be done automatically
import cython
cython.declare(Nodes=object, ExprNodes=object, EncodedString=object)

import os
import re
import sys
from types import ListType, TupleType
from Cython.Compiler.Scanning import PyrexScanner, FileSourceDescriptor
import Nodes
import ExprNodes
import StringEncoding
from StringEncoding import EncodedString, BytesLiteral
from ModuleNode import ModuleNode
from Errors import error, warning, InternalError
from Cython import Utils
import Future
import Options

class Ctx(object):
    #  Parsing context
    level = 'other'
    visibility = 'private'
    cdef_flag = 0
    typedef_flag = 0
    api = 0
    overridable = 0
    nogil = 0

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __call__(self, **kwds):
        ctx = Ctx()
        d = ctx.__dict__
        d.update(self.__dict__)
        d.update(kwds)
        return ctx

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
    n1 = p_sub_expr(s)
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
        s.expect('else')
        other = p_test(s)
        return ExprNodes.CondExprNode(pos, test=test, true_val=expr, false_val=other)
    else:
        return expr
        
#test: or_test | lambda_form
        
def p_test(s):
    return p_or_test(s)

#or_test: and_test ('or' and_test)*

def p_or_test(s):
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
    n1 = p_starred_expr(s)
    if s.sy in comparison_ops:
        pos = s.position()
        op = p_cmp_op(s)
        n2 = p_starred_expr(s)
        n1 = ExprNodes.PrimaryCmpNode(pos, 
            operator = op, operand1 = n1, operand2 = n2)
        if s.sy in comparison_ops:
            n1.cascade = p_cascaded_cmp(s)
    return n1

def p_starred_expr(s):
    pos = s.position()
    if s.sy == '*':
        starred = True
        s.next()
    else:
        starred = False
    expr = p_bit_expr(s)
    if starred:
        expr = ExprNodes.StarredTargetNode(pos, expr)
    return expr

def p_cascaded_cmp(s):
    pos = s.position()
    op = p_cmp_op(s)
    n2 = p_starred_expr(s)
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
    if base_type.name is None:
        s.error("Unknown type")
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
    # Here we decide if we are looking at an expression or type
    # If it is actually a type, but parsable as an expression, 
    # we treat it as an expression here. 
    if looking_at_expr(s):
        operand = p_simple_expr(s)
        node = ExprNodes.SizeofVarNode(pos, operand = operand)
    else:
        base_type = p_c_base_type(s)
        declarator = p_c_declarator(s, empty = 1)
        node = ExprNodes.SizeofTypeNode(pos, 
            base_type = base_type, declarator = declarator)
    s.expect(')')
    return node

def p_yield_expression(s):
    # s.sy == "yield"
    pos = s.position()
    s.next()
    if s.sy not in ('EOF', 'NEWLINE', ')'):
        expr = p_expr(s)
    s.error("generators ('yield') are not currently supported")
    return Nodes.PassStatNode(pos)

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
        name = EncodedString( p_ident(s) )
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
    while s.sy not in ('**', ')'):
        if s.sy == '*':
            if star_arg:
                s.error("only one star-arg parameter allowed",
                    pos = s.position())
            s.next()
            star_arg = p_simple_expr(s)
        else:
            arg = p_simple_expr(s)
            if s.sy == '=':
                s.next()
                if not arg.is_name:
                    s.error("Expected an identifier before '='",
                        pos = arg.pos)
                encoded_name = EncodedString(arg.name)
                keyword = ExprNodes.IdentifierStringNode(arg.pos, 
                    value = encoded_name)
                arg = p_simple_expr(s)
                keyword_args.append((keyword, arg))
            else:
                if keyword_args:
                    s.error("Non-keyword arg following keyword arg",
                        pos = arg.pos)
                if star_arg:
                    s.error("Non-keyword arg following star-arg",
                        pos = arg.pos)
                positional_args.append(arg)
        if s.sy != ',':
            break
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

#atom: '(' [testlist] ')' | '[' [listmaker] ']' | '{' [dict_or_set_maker] '}' | '`' testlist '`' | NAME | NUMBER | STRING+

def p_atom(s):
    pos = s.position()
    sy = s.sy
    if sy == '(':
        s.next()
        if s.sy == ')':
            result = ExprNodes.TupleNode(pos, args = [])
        elif s.sy == 'yield':
            result = p_yield_expression(s)
        else:
            result = p_expr(s)
        s.expect(')')
        return result
    elif sy == '[':
        return p_list_maker(s)
    elif sy == '{':
        return p_dict_or_set_maker(s)
    elif sy == '`':
        return p_backquote_expr(s)
    elif sy == 'INT':
        value = s.systring
        s.next()
        unsigned = ""
        longness = ""
        while value[-1] in "UuLl":
            if value[-1] in "Ll":
                longness += "L"
            else:
                unsigned += "U"
            value = value[:-1]
        return ExprNodes.IntNode(pos, 
                                 value = value,
                                 unsigned = unsigned,
                                 longness = longness)
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
        elif kind == 'u':
            return ExprNodes.UnicodeNode(pos, value = value)
        else:
            return ExprNodes.StringNode(pos, value = value)
    elif sy == 'IDENT':
        name = EncodedString( s.systring )
        s.next()
        if name == "None":
            return ExprNodes.NoneNode(pos)
        elif name == "True":
            return ExprNodes.BoolNode(pos, value=True)
        elif name == "False":
            return ExprNodes.BoolNode(pos, value=False)
        elif name == "NULL":
            return ExprNodes.NullNode(pos)
        else:
            return p_name(s, name)
    else:
        s.error("Expected an identifier or literal")

def p_name(s, name):
    pos = s.position()
    if not s.compile_time_expr and name in s.compile_time_env:
        value = s.compile_time_env.lookup_here(name)
        rep = repr(value)
        if isinstance(value, bool):
            return ExprNodes.BoolNode(pos, value = value)
        elif isinstance(value, int):
            return ExprNodes.IntNode(pos, value = rep)
        elif isinstance(value, long):
            return ExprNodes.IntNode(pos, value = rep, longness = "L")
        elif isinstance(value, float):
            return ExprNodes.FloatNode(pos, value = rep)
        elif isinstance(value, (str, unicode)):
            return ExprNodes.StringNode(pos, value = value)
        else:
            error(pos, "Invalid type for compile-time constant: %s"
                % value.__class__.__name__)
    return ExprNodes.NameNode(pos, name = name)

def p_cat_string_literal(s):
    # A sequence of one or more adjacent string literals.
    # Returns (kind, value) where kind in ('b', 'c', 'u')
    kind, value = p_string_literal(s)
    if kind != 'c':
        strings = [value]
        while s.sy == 'BEGIN_STRING':
            next_kind, next_value = p_string_literal(s)
            if next_kind == 'c':
                error(s.position(),
                      "Cannot concatenate char literal with another string or char literal")
            elif next_kind != kind:
                # we have to switch to unicode now
                if kind == 'b':
                    # concatenating a unicode string to byte strings
                    strings = [u''.join([s.decode(s.encoding) for s in strings])]
                elif kind == 'u':
                    # concatenating a byte string to unicode strings
                    strings.append(next_value.decode(next_value.encoding))
                kind = 'u'
            else:
                strings.append(next_value)
        if kind == 'u':
            value = EncodedString( u''.join(strings) )
        else:
            value = BytesLiteral( ''.join(strings) )
            value.encoding = s.source_encoding
    return kind, value

def p_opt_string_literal(s):
    if s.sy == 'BEGIN_STRING':
        return p_string_literal(s)
    else:
        return None

def p_string_literal(s):
    # A single string or char literal.
    # Returns (kind, value) where kind in ('b', 'c', 'u')
    # s.sy == 'BEGIN_STRING'
    pos = s.position()
    is_raw = 0
    kind = s.systring[:1].lower()
    if kind == 'r':
        kind = ''
        is_raw = 1
    elif kind in 'ub':
        is_raw = s.systring[1:2].lower() == 'r'
    elif kind != 'c':
        kind = ''
    if Future.unicode_literals in s.context.future_directives:
        if kind == '':
            kind = 'u'
    elif kind == '':
        kind = 'b'
    if kind == 'u':
        chars = StringEncoding.UnicodeLiteralBuilder()
    else:
        chars = StringEncoding.BytesLiteralBuilder(s.source_encoding)
    while 1:
        s.next()
        sy = s.sy
        #print "p_string_literal: sy =", sy, repr(s.systring) ###
        if sy == 'CHARS':
            chars.append(s.systring)
        elif sy == 'ESCAPE':
            has_escape = True
            systr = s.systring
            if is_raw:
                if systr == u'\\\n':
                    chars.append(u'\\\n')
                elif systr == u'\\\"':
                    chars.append(u'"')
                elif systr == u'\\\'':
                    chars.append(u"'")
                else:
                    chars.append(systr)
            else:
                c = systr[1]
                if c in u"01234567":
                    chars.append_charval( int(systr[1:], 8) )
                elif c in u"'\"\\":
                    chars.append(c)
                elif c in u"abfnrtv":
                    chars.append(
                        StringEncoding.char_from_escape_sequence(systr))
                elif c == u'\n':
                    pass
                elif c in u'Uux':
                    if kind == 'u' or c == 'x':
                        chrval = int(systr[2:], 16)
                        if chrval > 1114111: # sys.maxunicode:
                            s.error("Invalid unicode escape '%s'" % systr,
                                    pos = pos)
                        elif chrval > 65535:
                            warning(s.position(),
                                    "Unicode characters above 65535 are not "
                                    "necessarily portable across Python installations", 1)
                        chars.append_charval(chrval)
                    else:
                        # unicode escapes in plain byte strings are not unescaped
                        chars.append(systr)
                else:
                    chars.append(u'\\' + systr[1:])
        elif sy == 'NEWLINE':
            chars.append(u'\n')
        elif sy == 'END_STRING':
            break
        elif sy == 'EOF':
            s.error("Unclosed string literal", pos = pos)
        else:
            s.error(
                "Unexpected token %r:%r in string literal" %
                    (sy, s.systring))
    if kind == 'c':
        value = chars.getchar()
        if len(value) != 1:
            error(pos, u"invalid character literal: %r" % value)
    else:
        value = chars.getstring()
    s.next()
    #print "p_string_literal: value =", repr(value) ###
    return kind, value

# list_display      ::=      "[" [listmaker] "]"
# listmaker     ::=     expression ( list_for | ( "," expression )* [","] )
# list_iter     ::=     list_for | list_if
# list_for     ::=     "for" expression_list "in" testlist [list_iter]
# list_if     ::=     "if" test [list_iter]
        
def p_list_maker(s):
    # s.sy == '['
    pos = s.position()
    s.next()
    if s.sy == ']':
        s.expect(']')
        return ExprNodes.ListNode(pos, args = [])
    expr = p_simple_expr(s)
    if s.sy == 'for':
        target = ExprNodes.ListNode(pos, args = [])
        append = ExprNodes.ComprehensionAppendNode(
            pos, expr=expr, target=ExprNodes.CloneNode(target))
        loop = p_list_for(s, Nodes.ExprStatNode(append.pos, expr=append))
        s.expect(']')
        return ExprNodes.ComprehensionNode(
            pos, loop=loop, append=append, target=target)
    else:
        exprs = [expr]
        if s.sy == ',':
            s.next()
            exprs += p_simple_expr_list(s)
        s.expect(']')
        return ExprNodes.ListNode(pos, args = exprs)
        
def p_list_iter(s, body):
    if s.sy == 'for':
        return p_list_for(s, body)
    elif s.sy == 'if':
        return p_list_if(s, body)
    else:
        # insert the 'append' operation into the loop
        return body

def p_list_for(s, body):
    # s.sy == 'for'
    pos = s.position()
    s.next()
    kw = p_for_bounds(s)
    kw['else_clause'] = None
    kw['body'] = p_list_iter(s, body)
    return Nodes.ForStatNode(pos, **kw)
        
def p_list_if(s, body):
    # s.sy == 'if'
    pos = s.position()
    s.next()
    test = p_test(s)
    return Nodes.IfStatNode(pos, 
        if_clauses = [Nodes.IfClauseNode(pos, condition = test,
                                         body = p_list_iter(s, body))],
        else_clause = None )

#dictmaker: test ':' test (',' test ':' test)* [',']

def p_dict_or_set_maker(s):
    # s.sy == '{'
    pos = s.position()
    s.next()
    if s.sy == '}':
        s.next()
        return ExprNodes.DictNode(pos, key_value_pairs = [])
    item = p_simple_expr(s)
    if s.sy == ',' or s.sy == '}':
        # set literal
        values = [item]
        while s.sy == ',':
            s.next()
            if s.sy == '}':
                break
            values.append( p_simple_expr(s) )
        s.expect('}')
        return ExprNodes.SetNode(pos, args=values)
    elif s.sy == 'for':
        # set comprehension
        target = ExprNodes.SetNode(pos, args=[])
        append = ExprNodes.ComprehensionAppendNode(
            item.pos, expr=item, target=ExprNodes.CloneNode(target))
        loop = p_list_for(s, Nodes.ExprStatNode(append.pos, expr=append))
        s.expect('}')
        return ExprNodes.ComprehensionNode(
            pos, loop=loop, append=append, target=target)
    elif s.sy == ':':
        # dict literal or comprehension
        key = item
        s.next()
        value = p_simple_expr(s)
        if s.sy == 'for':
            # dict comprehension
            target = ExprNodes.DictNode(pos, key_value_pairs = [])
            append = ExprNodes.DictComprehensionAppendNode(
                item.pos, key_expr=key, value_expr=value,
                target=ExprNodes.CloneNode(target))
            loop = p_list_for(s, Nodes.ExprStatNode(append.pos, expr=append))
            s.expect('}')
            return ExprNodes.ComprehensionNode(
                pos, loop=loop, append=append, target=target)
        else:
            # dict literal
            items = [ExprNodes.DictItemNode(key.pos, key=key, value=value)]
            while s.sy == ',':
                s.next()
                if s.sy == '}':
                    break
                key = p_simple_expr(s)
                s.expect(':')
                value = p_simple_expr(s)
                items.append(
                    ExprNodes.DictItemNode(key.pos, key=key, value=value))
            s.expect('}')
            return ExprNodes.DictNode(pos, key_value_pairs=items)
    else:
        # raise an error
        s.expect('}')
    return ExprNodes.DictNode(pos, key_value_pairs = [])

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
        expr = p_simple_expr(s)
        exprs.append(expr)
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
        if re.match(r"([+*/\%^\&|-]|<<|>>|\*\*|//)=", s.sy):
            lhs = expr_list[0]
            if not isinstance(lhs, (ExprNodes.AttributeNode, ExprNodes.IndexNode, ExprNodes.NameNode) ):
                error(lhs.pos, "Illegal operand for inplace operation.")
            operator = s.sy[:-1]
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
    #  The input is a list of expression nodes, representing the LHSs
    #  and RHS of one (possibly cascaded) assignment statement.  For
    #  sequence constructors, rearranges the matching parts of both
    #  sides into a list of equivalent assignments between the
    #  individual elements.  This transformation is applied
    #  recursively, so that nested structures get matched as well.
    rhs = input[-1]
    if not rhs.is_sequence_constructor:
        output.append(input)
        return

    rhs_size = len(rhs.args)
    lhs_targets = [ [] for _ in range(rhs_size) ]
    starred_assignments = []
    for lhs in input[:-1]:
        if not lhs.is_sequence_constructor:
            if lhs.is_starred:
                error(lhs.pos, "starred assignment target must be in a list or tuple")
            output.append([lhs,rhs])
            continue
        lhs_size = len(lhs.args)
        starred_targets = sum([1 for expr in lhs.args if expr.is_starred])
        if starred_targets:
            if starred_targets > 1:
                error(lhs.pos, "more than 1 starred expression in assignment")
                output.append([lhs,rhs])
                continue
            elif lhs_size - starred_targets > rhs_size:
                error(lhs.pos, "need more than %d value%s to unpack"
                      % (rhs_size, (rhs_size != 1) and 's' or ''))
                output.append([lhs,rhs])
                continue
            map_starred_assignment(lhs_targets, starred_assignments,
                                   lhs.args, rhs.args)
        else:
            if lhs_size > rhs_size:
                error(lhs.pos, "need more than %d value%s to unpack"
                      % (rhs_size, (rhs_size != 1) and 's' or ''))
                output.append([lhs,rhs])
                continue
            elif lhs_size < rhs_size:
                error(lhs.pos, "too many values to unpack (expected %d, got %d)"
                      % (lhs_size, rhs_size))
                output.append([lhs,rhs])
                continue
            else:
                for targets, expr in zip(lhs_targets, lhs.args):
                    targets.append(expr)

    # recursively flatten partial assignments
    for cascade, rhs in zip(lhs_targets, rhs.args):
        if cascade:
            cascade.append(rhs)
            flatten_parallel_assignments(cascade, output)

    # recursively flatten starred assignments
    for cascade in starred_assignments:
        if cascade[0].is_sequence_constructor:
            flatten_parallel_assignments(cascade, output)
        else:
            output.append(cascade)

def map_starred_assignment(lhs_targets, starred_assignments, lhs_args, rhs_args):
    # Appends the fixed-position LHS targets to the target list that
    # appear left and right of the starred argument.
    #
    # The starred_assignments list receives a new tuple
    # (lhs_target, rhs_values_list) that maps the remaining arguments
    # (those that match the starred target) to a list.

    # left side of the starred target
    for i, (targets, expr) in enumerate(zip(lhs_targets, lhs_args)):
        if expr.is_starred:
            starred = i
            lhs_remaining = len(lhs_args) - i - 1
            break
        targets.append(expr)
    else:
        raise InternalError("no starred arg found when splitting starred assignment")

    # right side of the starred target
    for i, (targets, expr) in enumerate(zip(lhs_targets[-lhs_remaining:],
                                            lhs_args[-lhs_remaining:])):
        targets.append(expr)

    # the starred target itself, must be assigned a (potentially empty) list
    target = lhs_args[starred].target # unpack starred node
    starred_rhs = rhs_args[starred:]
    if lhs_remaining:
        starred_rhs = starred_rhs[:-lhs_remaining]
    if starred_rhs:
        pos = starred_rhs[0].pos
    else:
        pos = target.pos
    starred_assignments.append([
        target, ExprNodes.ListNode(pos=pos, args=starred_rhs)])


def p_print_statement(s):
    # s.sy == 'print'
    pos = s.position()
    s.next()
    if s.sy == '>>':
        s.error("'print >>' not yet implemented")
    args = []
    ends_with_comma = 0
    if s.sy not in ('NEWLINE', 'EOF'):
        args.append(p_simple_expr(s))
        while s.sy == ',':
            s.next()
            if s.sy in ('NEWLINE', 'EOF'):
                ends_with_comma = 1
                break
            args.append(p_simple_expr(s))
    arg_tuple = ExprNodes.TupleNode(pos, args = args)
    return Nodes.PrintStatNode(pos,
        arg_tuple = arg_tuple, append_newline = not ends_with_comma)

def p_exec_statement(s):
    # s.sy == 'exec'
    pos = s.position()
    s.next()
    args = [ p_bit_expr(s) ]
    if s.sy == 'in':
        s.next()
        args.append(p_simple_expr(s))
        if s.sy == ',':
            s.next()
            args.append(p_simple_expr(s))
    else:
        error(pos, "'exec' currently requires a target mapping (globals/locals)")
    return Nodes.ExecStatNode(pos, args = args)

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
        dotted_name = EncodedString(dotted_name)
        if kind == 'cimport':
            stat = Nodes.CImportStatNode(pos, 
                module_name = dotted_name,
                as_name = as_name)
        else:
            if as_name and "." in dotted_name:
                name_list = ExprNodes.ListNode(pos, args = [
                        ExprNodes.IdentifierStringNode(
                            pos, value = EncodedString("*"))])
            else:
                name_list = None
            stat = Nodes.SingleAssignmentNode(pos,
                lhs = ExprNodes.NameNode(pos, 
                    name = as_name or target_name),
                rhs = ExprNodes.ImportNode(pos, 
                    module_name = ExprNodes.IdentifierStringNode(
                        pos, value = dotted_name),
                    name_list = name_list))
        stats.append(stat)
    return Nodes.StatListNode(pos, stats = stats)

def p_from_import_statement(s, first_statement = 0):
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
    is_cimport = kind == 'cimport'
    is_parenthesized = False
    if s.sy == '*':
        imported_names = [(s.position(), "*", None, None)]
        s.next()
    else:
        if s.sy == '(':
            is_parenthesized = True
            s.next()
        imported_names = [p_imported_name(s, is_cimport)]
    while s.sy == ',':
        s.next()
        imported_names.append(p_imported_name(s, is_cimport))
    if is_parenthesized:
        s.expect(')')
    dotted_name = EncodedString(dotted_name)
    if dotted_name == '__future__':
        if not first_statement:
            s.error("from __future__ imports must occur at the beginning of the file")
        else:
            for (name_pos, name, as_name, kind) in imported_names:
                if name == "braces":
                    s.error("not a chance", name_pos)
                    break
                try:
                    directive = getattr(Future, name)
                except AttributeError:
                    s.error("future feature %s is not defined" % name, name_pos)
                    break
                s.context.future_directives.add(directive)
        return Nodes.PassStatNode(pos)
    elif kind == 'cimport':
        return Nodes.FromCImportStatNode(pos,
            module_name = dotted_name,
            imported_names = imported_names)
    else:
        imported_name_strings = []
        items = []
        for (name_pos, name, as_name, kind) in imported_names:
            encoded_name = EncodedString(name)
            imported_name_strings.append(
                ExprNodes.IdentifierStringNode(name_pos, value = encoded_name))
            items.append(
                (name,
                 ExprNodes.NameNode(name_pos, 
                                    name = as_name or name)))
        import_list = ExprNodes.ListNode(
            imported_names[0][0], args = imported_name_strings)
        dotted_name = EncodedString(dotted_name)
        return Nodes.FromImportStatNode(pos,
            module = ExprNodes.ImportNode(dotted_name_pos,
                module_name = ExprNodes.IdentifierStringNode(pos, value = dotted_name),
                name_list = import_list),
            items = items)

imported_name_kinds = ('class', 'struct', 'union')

def p_imported_name(s, is_cimport):
    pos = s.position()
    kind = None
    if is_cimport and s.systring in imported_name_kinds:
        kind = s.systring
        s.next()
    name = p_ident(s)
    as_name = p_as_name(s)
    return (pos, name, as_name, kind)

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
    return (pos, target_name, u'.'.join(names), as_name)

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
    else:
        if s.sy == 'from':
            s.next()
            bound1 = p_bit_expr(s)
        else:
            # Support shorter "for a <= x < b" syntax
            bound1, target = target, None
        rel1 = p_for_from_relation(s)
        name2_pos = s.position()
        name2 = p_ident(s)
        rel2_pos = s.position()
        rel2 = p_for_from_relation(s)
        bound2 = p_bit_expr(s)
        step = p_for_from_step(s)
        if target is None:
            target = ExprNodes.NameNode(name2_pos, name = name2)
        else:
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

def p_target(s, terminator):
    pos = s.position()
    expr = p_starred_expr(s)
    if s.sy == ',':
        s.next()
        exprs = [expr]
        while s.sy != terminator:
            exprs.append(p_starred_expr(s))
            if s.sy != ',':
                break
            s.next()
        return ExprNodes.TupleNode(pos, args = exprs)
    else:
        return expr

def p_for_target(s):
    return p_target(s, 'in')

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

def p_include_statement(s, ctx):
    pos = s.position()
    s.next() # 'include'
    _, include_file_name = p_string_literal(s)
    s.expect_newline("Syntax error in include statement")
    if s.compile_time_eval:
        include_file_path = s.context.find_include_file(include_file_name, pos)
        if include_file_path:
            s.included_files.append(include_file_name)
            f = Utils.open_source_file(include_file_path, mode="rU")
            source_desc = FileSourceDescriptor(include_file_path)
            s2 = PyrexScanner(f, source_desc, s, source_encoding=f.encoding, parse_comments=s.parse_comments)
            try:
                tree = p_statement_list(s2, ctx)
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
#    if s.sy == 'IDENT' and s.systring in ('gil', 'nogil'):
    if s.sy == 'IDENT' and s.systring == 'nogil':
        state = s.systring
        s.next()
        body = p_suite(s)
        return Nodes.GILStatNode(pos, state = state, body = body)
    else:
        manager = p_expr(s)
        target = None
        if s.sy == 'IDENT' and s.systring == 'as':
            s.next()
            allow_multi = (s.sy == '(')
            target = p_target(s, ':')
            if not allow_multi and isinstance(target, ExprNodes.TupleNode):
                s.error("Multiple with statement target values not allowed without paranthesis")
        body = p_suite(s)
    return Nodes.WithStatNode(pos, manager = manager, 
                              target = target, body = body)
    
def p_simple_statement(s, first_statement = 0):
    #print "p_simple_statement:", s.sy, s.systring ###
    if s.sy == 'global':
        node = p_global_statement(s)
    elif s.sy == 'print':
        node = p_print_statement(s)
    elif s.sy == 'exec':
        node = p_exec_statement(s)
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
        node = p_from_import_statement(s, first_statement = first_statement)
    elif s.sy == 'yield':
        node = p_yield_expression(s)
    elif s.sy == 'assert':
        node = p_assert_statement(s)
    elif s.sy == 'pass':
        node = p_pass_statement(s)
    else:
        node = p_expression_or_assignment(s)
    return node

def p_simple_statement_list(s, ctx, first_statement = 0):
    # Parse a series of simple statements on one line
    # separated by semicolons.
    stat = p_simple_statement(s, first_statement = first_statement)
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

def p_IF_statement(s, ctx):
    pos = s.position()
    saved_eval = s.compile_time_eval
    current_eval = saved_eval
    denv = s.compile_time_env
    result = None
    while 1:
        s.next() # 'IF' or 'ELIF'
        expr = p_compile_time_expr(s)
        s.compile_time_eval = current_eval and bool(expr.compile_time_value(denv))
        body = p_suite(s, ctx)
        if s.compile_time_eval:
            result = body
            current_eval = 0
        if s.sy != 'ELIF':
            break
    if s.sy == 'ELSE':
        s.next()
        s.compile_time_eval = current_eval
        body = p_suite(s, ctx)
        if current_eval:
            result = body
    if not result:
        result = Nodes.PassStatNode(pos)
    s.compile_time_eval = saved_eval
    return result

def p_statement(s, ctx, first_statement = 0):
    cdef_flag = ctx.cdef_flag
    decorators = None
    if s.sy == 'ctypedef':
        if ctx.level not in ('module', 'module_pxd'):
            s.error("ctypedef statement not allowed here")
        #if ctx.api:
        #    error(s.position(), "'api' not allowed with 'ctypedef'")
        return p_ctypedef_statement(s, ctx)
    elif s.sy == 'DEF':
        return p_DEF_statement(s)
    elif s.sy == 'IF':
        return p_IF_statement(s, ctx)
    elif s.sy == 'DECORATOR':
        if ctx.level not in ('module', 'class', 'c_class', 'property', 'module_pxd', 'c_class_pxd'):
            print ctx.level
            s.error('decorator not allowed here')
        s.level = ctx.level
        decorators = p_decorators(s)
        if s.sy not in ('def', 'cdef', 'cpdef'):
            s.error("Decorators can only be followed by functions ")
    elif s.sy == 'pass' and cdef_flag:
        # empty cdef block
        return p_pass_statement(s, with_newline = 1)

    overridable = 0
    if s.sy == 'cdef':
        cdef_flag = 1
        s.next()
    elif s.sy == 'cpdef':
        cdef_flag = 1
        overridable = 1
        s.next()
    if cdef_flag:
        if ctx.level not in ('module', 'module_pxd', 'function', 'c_class', 'c_class_pxd'):
            s.error('cdef statement not allowed here')
        s.level = ctx.level
        node = p_cdef_statement(s, ctx(overridable = overridable))
        if decorators is not None:
            if not isinstance(node, (Nodes.CFuncDefNode, Nodes.CVarDefNode)):
                s.error("Decorators can only be followed by functions ")
            node.decorators = decorators
        return node
    else:
        if ctx.api:
            error(s.pos, "'api' not allowed with this statement")
        elif s.sy == 'def':
            if ctx.level not in ('module', 'class', 'c_class', 'c_class_pxd', 'property'):
                s.error('def statement not allowed here')
            s.level = ctx.level
            return p_def_statement(s, decorators)
        elif s.sy == 'class':
            if ctx.level != 'module':
                s.error("class definition not allowed here")
            return p_class_statement(s)
        elif s.sy == 'include':
            if ctx.level not in ('module', 'module_pxd'):
                s.error("include statement not allowed here")
            return p_include_statement(s, ctx)
        elif ctx.level == 'c_class' and s.sy == 'IDENT' and s.systring == 'property':
            return p_property_decl(s)
        elif s.sy == 'pass' and ctx.level != 'property':
            return p_pass_statement(s, with_newline = 1)
        else:
            if ctx.level in ('c_class_pxd', 'property'):
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
                return p_simple_statement_list(
                    s, ctx, first_statement = first_statement)

def p_statement_list(s, ctx, first_statement = 0):
    # Parse a series of statements separated by newlines.
    pos = s.position()
    stats = []
    while s.sy not in ('DEDENT', 'EOF'):
        stats.append(p_statement(s, ctx, first_statement = first_statement))
        first_statement = 0
    if len(stats) == 1:
        return stats[0]
    else:
        return Nodes.StatListNode(pos, stats = stats)

def p_suite(s, ctx = Ctx(), with_doc = 0, with_pseudo_doc = 0):
    pos = s.position()
    s.expect(':')
    doc = None
    stmts = []
    if s.sy == 'NEWLINE':
        s.next()
        s.expect_indent()
        if with_doc or with_pseudo_doc:
            doc = p_doc_string(s)
        body = p_statement_list(s, ctx)
        s.expect_dedent()
    else:
        if ctx.api:
            error(s.pos, "'api' not allowed with this statement")
        if ctx.level in ('module', 'class', 'function', 'other'):
            body = p_simple_statement_list(s, ctx)
        else:
            body = p_pass_statement(s)
            s.expect_newline("Syntax error in declarations")
    if with_doc:
        return doc, body
    else:
        return body

def p_positional_and_keyword_args(s, end_sy_set, type_positions=(), type_keywords=()):
    """
    Parses positional and keyword arguments. end_sy_set
    should contain any s.sy that terminate the argument list.
    Argument expansion (* and **) are not allowed.

    type_positions and type_keywords specifies which argument
    positions and/or names which should be interpreted as
    types. Other arguments will be treated as expressions.

    Returns: (positional_args, keyword_args)
    """
    positional_args = []
    keyword_args = []
    pos_idx = 0

    while s.sy not in end_sy_set:
        if s.sy == '*' or s.sy == '**':
            s.error('Argument expansion not allowed here.')

        was_keyword = False
        parsed_type = False
        if s.sy == 'IDENT':
            # Since we can have either types or expressions as positional args,
            # we use a strategy of looking an extra step forward for a '=' and
            # if it is a positional arg we backtrack.
            ident = s.systring
            s.next()
            if s.sy == '=':
                s.next()
                # Is keyword arg
                if ident in type_keywords:
                    arg = p_c_base_type(s)
                    parsed_type = True
                else:
                    arg = p_simple_expr(s)
                keyword_node = ExprNodes.IdentifierStringNode(arg.pos,
                                value = EncodedString(ident))
                keyword_args.append((keyword_node, arg))
                was_keyword = True
            else:
                s.put_back('IDENT', ident)
                
        if not was_keyword:
            if pos_idx in type_positions:
                arg = p_c_base_type(s)
                parsed_type = True
            else:
                arg = p_simple_expr(s)
            positional_args.append(arg)
            pos_idx += 1
            if len(keyword_args) > 0:
                s.error("Non-keyword arg following keyword arg",
                        pos = arg.pos)

        if s.sy != ',':
            if s.sy not in end_sy_set:
                if parsed_type:
                    s.error("Expected: type")
                else:
                    s.error("Expected: expression")
            break
        s.next()
    return positional_args, keyword_args

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

calling_convention_words = ("__stdcall", "__cdecl", "__fastcall")

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
    #print "p_c_simple_base_type: self_flag =", self_flag, nonempty
    is_basic = 0
    signed = 1
    longness = 0
    complex = 0
    module_path = []
    pos = s.position()
    if not s.sy == 'IDENT':
        error(pos, "Expected an identifier, found '%s'" % s.sy)
    if looking_at_base_type(s):
        #print "p_c_simple_base_type: looking_at_base_type at", s.position()
        is_basic = 1
        if s.sy == 'IDENT' and s.systring in special_basic_c_types:
            signed, longness = special_basic_c_types[s.systring]
            name = s.systring
            s.next()
        else:
            signed, longness = p_sign_and_longness(s)
            if s.sy == 'IDENT' and s.systring in basic_c_type_names:
                name = s.systring
                s.next()
            else:
                name = 'int'
        if s.sy == 'IDENT' and s.systring == 'complex':
            complex = 1
            s.next()
    elif looking_at_dotted_name(s):
        #print "p_c_simple_base_type: looking_at_type_name at", s.position()
        name = s.systring
        s.next()
        while s.sy == '.':
            module_path.append(name)
            s.next()
            name = p_ident(s)
    else:
        name = s.systring
        s.next()
        if nonempty and s.sy != 'IDENT':
            # Make sure this is not a declaration of a variable or function.  
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
    
    type_node = Nodes.CSimpleBaseTypeNode(pos, 
        name = name, module_path = module_path,
        is_basic_c_type = is_basic, signed = signed,
        complex = complex, longness = longness, 
        is_self_arg = self_flag)


    # Treat trailing [] on type as buffer access if it appears in a context
    # where declarator names are required (so that it cannot mean int[] or
    # sizeof(int[SIZE]))...
    #
    # (This means that buffers cannot occur where there can be empty declarators,
    # which is an ok restriction to make.)
    if nonempty and s.sy == '[':
        return p_buffer_access(s, type_node)
    else:
        return type_node

def p_buffer_access(s, base_type_node):
    # s.sy == '['
    pos = s.position()
    s.next()
    positional_args, keyword_args = (
        p_positional_and_keyword_args(s, (']',), (0,), ('dtype',))
    )
    s.expect(']')

    keyword_dict = ExprNodes.DictNode(pos,
        key_value_pairs = [
            ExprNodes.DictItemNode(pos=key.pos, key=key, value=value)
            for key, value in keyword_args
        ])

    result = Nodes.CBufferAccessTypeNode(pos,
        positional_args = positional_args,
        keyword_args = keyword_dict,
        base_type_node = base_type_node)
    return result
    

def looking_at_name(s):
    return s.sy == 'IDENT' and not s.systring in calling_convention_words

def looking_at_expr(s):
    if s.systring in base_type_start_words:
        return False
    elif s.sy == 'IDENT':
        is_type = False
        name = s.systring
        dotted_path = []
        s.next()
        while s.sy == '.':
            s.next()
            dotted_path.append(s.systring)
            s.expect('IDENT')
        saved = s.sy, s.systring
        if s.sy == 'IDENT':
            is_type = True
        elif s.sy == '*' or s.sy == '**':
            s.next()
            is_type = s.sy == ')'
            s.put_back(*saved)
        elif s.sy == '(':
            s.next()
            is_type = s.sy == '*'
            s.put_back(*saved)
        elif s.sy == '[':
            s.next()
            is_type = s.sy == ']'
            s.put_back(*saved)
        dotted_path.reverse()
        for p in dotted_path:
            s.put_back('IDENT', p)
            s.put_back('.', '.')
        s.put_back('IDENT', name)
        return not is_type
    else:
        return True

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

basic_c_type_names = ("void", "char", "int", "float", "double", "bint")

special_basic_c_types = {
    # name : (signed, longness)
    "Py_ssize_t" : (2, 0),
    "size_t"     : (0, 0),
}

sign_and_longness_words = ("short", "long", "signed", "unsigned")

base_type_start_words = \
    basic_c_type_names + sign_and_longness_words + tuple(special_basic_c_types)

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

def p_c_declarator(s, ctx = Ctx(), empty = 0, is_type = 0, cmethod_flag = 0,
                   assignable = 0, nonempty = 0,
                   calling_convention_allowed = 0):
    # If empty is true, the declarator must be empty. If nonempty is true,
    # the declarator must be nonempty. Otherwise we don't care.
    # If cmethod_flag is true, then if this declarator declares
    # a function, it's a C method of an extension type.
    pos = s.position()
    if s.sy == '(':
        s.next()
        if s.sy == ')' or looking_at_name(s):
            base = Nodes.CNameDeclaratorNode(pos, name = EncodedString(u""), cname = None)
            result = p_c_func_declarator(s, pos, ctx, base, cmethod_flag)
        else:
            result = p_c_declarator(s, ctx, empty = empty, is_type = is_type,
                                    cmethod_flag = cmethod_flag,
                                    nonempty = nonempty,
                                    calling_convention_allowed = 1)
            s.expect(')')
    else:
        result = p_c_simple_declarator(s, ctx, empty, is_type, cmethod_flag,
                                       assignable, nonempty)
    if not calling_convention_allowed and result.calling_convention and s.sy != '(':
        error(s.position(), "%s on something that is not a function"
            % result.calling_convention)
    while s.sy in ('[', '('):
        pos = s.position()
        if s.sy == '[':
            result = p_c_array_declarator(s, result)
        else: # sy == '('
            s.next()
            result = p_c_func_declarator(s, pos, ctx, result, cmethod_flag)
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

def p_c_func_declarator(s, pos, ctx, base, cmethod_flag):
    #  Opening paren has already been skipped
    args = p_c_arg_list(s, ctx, cmethod_flag = cmethod_flag,
                        nonempty_declarators = 0)
    ellipsis = p_optional_ellipsis(s)
    s.expect(')')
    nogil = p_nogil(s)
    exc_val, exc_check = p_exception_value_clause(s)
    with_gil = p_with_gil(s)
    return Nodes.CFuncDeclaratorNode(pos, 
        base = base, args = args, has_varargs = ellipsis,
        exception_value = exc_val, exception_check = exc_check,
        nogil = nogil or ctx.nogil or with_gil, with_gil = with_gil)

def p_c_simple_declarator(s, ctx, empty, is_type, cmethod_flag,
                          assignable, nonempty):
    pos = s.position()
    calling_convention = p_calling_convention(s)
    if s.sy == '*':
        s.next()
        base = p_c_declarator(s, ctx, empty = empty, is_type = is_type,
                              cmethod_flag = cmethod_flag,
                              assignable = assignable, nonempty = nonempty)
        result = Nodes.CPtrDeclaratorNode(pos, 
            base = base)
    elif s.sy == '**': # scanner returns this as a single token
        s.next()
        base = p_c_declarator(s, ctx, empty = empty, is_type = is_type,
                              cmethod_flag = cmethod_flag,
                              assignable = assignable, nonempty = nonempty)
        result = Nodes.CPtrDeclaratorNode(pos,
            base = Nodes.CPtrDeclaratorNode(pos,
                base = base))
    else:
        rhs = None
        if s.sy == 'IDENT':
            name = EncodedString(s.systring)
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
            name = name, cname = cname, default = rhs)
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

def p_c_arg_list(s, ctx = Ctx(), in_pyfunc = 0, cmethod_flag = 0,
                 nonempty_declarators = 0, kw_only = 0):
    #  Comma-separated list of C argument declarations, possibly empty.
    #  May have a trailing comma.
    args = []
    is_self_arg = cmethod_flag
    while s.sy not in c_arg_list_terminators:
        args.append(p_c_arg_decl(s, ctx, in_pyfunc, is_self_arg,
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

def p_c_arg_decl(s, ctx, in_pyfunc, cmethod_flag = 0, nonempty = 0, kw_only = 0):
    pos = s.position()
    not_none = 0
    default = None
    base_type = p_c_base_type(s, cmethod_flag, nonempty = nonempty)
    declarator = p_c_declarator(s, ctx, nonempty = nonempty)
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
            default = ExprNodes.BoolNode(1)
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

def p_cdef_statement(s, ctx):
    pos = s.position()
    ctx.visibility = p_visibility(s, ctx.visibility)
    ctx.api = ctx.api or p_api(s)
    if ctx.api:
        if ctx.visibility not in ('private', 'public'):
            error(pos, "Cannot combine 'api' with '%s'" % ctx.visibility)
    if (ctx.visibility == 'extern') and s.sy == 'from':
        return p_cdef_extern_block(s, pos, ctx)
    elif s.sy == 'import':
        s.next()
        return p_cdef_extern_block(s, pos, ctx)
    elif p_nogil(s):
        ctx.nogil = 1
        if ctx.overridable:
            error(pos, "cdef blocks cannot be declared cpdef")
        return p_cdef_block(s, ctx)
    elif s.sy == ':':
        if ctx.overridable:
            error(pos, "cdef blocks cannot be declared cpdef")
        return p_cdef_block(s, ctx)
    elif s.sy == 'class':
        if ctx.level not in ('module', 'module_pxd'):
            error(pos, "Extension type definition not allowed here")
        if ctx.overridable:
            error(pos, "Extension types cannot be declared cpdef")
        return p_c_class_definition(s, pos, ctx)
    elif s.sy == 'IDENT' and s.systring in ("struct", "union", "enum", "packed"):
        if ctx.level not in ('module', 'module_pxd'):
            error(pos, "C struct/union/enum definition not allowed here")
        if ctx.overridable:
            error(pos, "C struct/union/enum cannot be declared cpdef")
        if s.systring == "enum":
            return p_c_enum_definition(s, pos, ctx)
        else:
            return p_c_struct_or_union_definition(s, pos, ctx)
    else:
        return p_c_func_or_var_declaration(s, pos, ctx)

def p_cdef_block(s, ctx):
    return p_suite(s, ctx(cdef_flag = 1))

def p_cdef_extern_block(s, pos, ctx):
    if ctx.overridable:
        error(pos, "cdef extern blocks cannot be declared cpdef")
    include_file = None
    s.expect('from')
    if s.sy == '*':
        s.next()
    else:
        _, include_file = p_string_literal(s)
    ctx = ctx(cdef_flag = 1, visibility = 'extern')
    if p_nogil(s):
        ctx.nogil = 1
    body = p_suite(s, ctx)
    return Nodes.CDefExternNode(pos,
        include_file = include_file,
        body = body)

def p_c_enum_definition(s, pos, ctx):
    # s.sy == ident 'enum'
    s.next()
    if s.sy == 'IDENT':
        name = s.systring
        s.next()
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
    return Nodes.CEnumDefNode(
        pos, name = name, cname = cname, items = items,
        typedef_flag = ctx.typedef_flag, visibility = ctx.visibility,
        in_pxd = ctx.level == 'module_pxd')

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

def p_c_struct_or_union_definition(s, pos, ctx):
    packed = False
    if s.systring == 'packed':
        packed = True
        s.next()
        if s.sy != 'IDENT' or s.systring != 'struct':
            s.expected('struct')
    # s.sy == ident 'struct' or 'union'
    kind = s.systring
    s.next()
    name = p_ident(s)
    cname = p_opt_cname(s)
    attributes = None
    if s.sy == ':':
        s.next()
        s.expect('NEWLINE')
        s.expect_indent()
        attributes = []
        body_ctx = Ctx()
        while s.sy != 'DEDENT':
            if s.sy != 'pass':
                attributes.append(
                    p_c_func_or_var_declaration(s, s.position(), body_ctx))
            else:
                s.next()
                s.expect_newline("Expected a newline")
        s.expect_dedent()
    else:
        s.expect_newline("Syntax error in struct or union definition")
    return Nodes.CStructOrUnionDefNode(pos, 
        name = name, cname = cname, kind = kind, attributes = attributes,
        typedef_flag = ctx.typedef_flag, visibility = ctx.visibility,
        in_pxd = ctx.level == 'module_pxd', packed = packed)

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

def p_c_func_or_var_declaration(s, pos, ctx):
    cmethod_flag = ctx.level in ('c_class', 'c_class_pxd')
    modifiers = p_c_modifiers(s)
    base_type = p_c_base_type(s, nonempty = 1)
    declarator = p_c_declarator(s, ctx, cmethod_flag = cmethod_flag,
                                assignable = 1, nonempty = 1)
    declarator.overridable = ctx.overridable
    if s.sy == ':':
        if ctx.level not in ('module', 'c_class', 'module_pxd', 'c_class_pxd'):
            s.error("C function definition not allowed here")
        doc, suite = p_suite(s, Ctx(level = 'function'), with_doc = 1)
        result = Nodes.CFuncDefNode(pos,
            visibility = ctx.visibility,
            base_type = base_type,
            declarator = declarator, 
            body = suite,
            doc = doc,
            modifiers = modifiers,
            api = ctx.api,
            overridable = ctx.overridable)
    else:
        #if api:
        #    error(s.pos, "'api' not allowed with variable declaration")
        declarators = [declarator]
        while s.sy == ',':
            s.next()
            if s.sy == 'NEWLINE':
                break
            declarator = p_c_declarator(s, ctx, cmethod_flag = cmethod_flag,
                                        assignable = 1, nonempty = 1)
            declarators.append(declarator)
        s.expect_newline("Syntax error in C variable declaration")
        result = Nodes.CVarDefNode(pos, 
            visibility = ctx.visibility,
            base_type = base_type,
            declarators = declarators,
            in_pxd = ctx.level == 'module_pxd',
            api = ctx.api,
            overridable = ctx.overridable)
    return result

def p_ctypedef_statement(s, ctx):
    # s.sy == 'ctypedef'
    pos = s.position()
    s.next()
    visibility = p_visibility(s, ctx.visibility)
    api = p_api(s)
    ctx = ctx(typedef_flag = 1, visibility = visibility)
    if api:
        ctx.api = 1
    if s.sy == 'class':
        return p_c_class_definition(s, pos, ctx)
    elif s.sy == 'IDENT' and s.systring in ('packed', 'struct', 'union', 'enum'):
        if s.systring == 'enum':
            return p_c_enum_definition(s, pos, ctx)
        else:
            return p_c_struct_or_union_definition(s, pos, ctx)
    else:
        base_type = p_c_base_type(s, nonempty = 1)
        if base_type.name is None:
            s.error("Syntax error in ctypedef statement")
        declarator = p_c_declarator(s, ctx, is_type = 1, nonempty = 1)
        s.expect_newline("Syntax error in ctypedef statement")
        return Nodes.CTypeDefNode(
            pos, base_type = base_type,
            declarator = declarator, visibility = visibility,
            in_pxd = ctx.level == 'module_pxd')

def p_decorators(s):
    decorators = []
    while s.sy == 'DECORATOR':
        pos = s.position()
        s.next()
        decstring = p_dotted_name(s, as_allowed=0)[2]
        names = decstring.split('.')
        decorator = ExprNodes.NameNode(pos, name=EncodedString(names[0]))
        for name in names[1:]:
            decorator = ExprNodes.AttributeNode(pos,
                                           attribute=EncodedString(name),
                                           obj=decorator)
        if s.sy == '(':
            decorator = p_call(s, decorator)
        decorators.append(Nodes.DecoratorNode(pos, decorator=decorator))
        s.expect_newline("Expected a newline after decorator")
    return decorators

def p_def_statement(s, decorators=None):
    # s.sy == 'def'
    pos = s.position()
    s.next()
    name = EncodedString( p_ident(s) )
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
    doc, body = p_suite(s, Ctx(level = 'function'), with_doc = 1)
    return Nodes.DefNode(pos, name = name, args = args, 
        star_arg = star_arg, starstar_arg = starstar_arg,
        doc = doc, body = body, decorators = decorators)

def p_py_arg_decl(s):
    pos = s.position()
    name = p_ident(s)
    return Nodes.PyArgDeclNode(pos, name = name)

def p_class_statement(s):
    # s.sy == 'class'
    pos = s.position()
    s.next()
    class_name = EncodedString( p_ident(s) )
    class_name.encoding = s.source_encoding
    if s.sy == '(':
        s.next()
        base_list = p_simple_expr_list(s)
        s.expect(')')
    else:
        base_list = []
    doc, body = p_suite(s, Ctx(level = 'class'), with_doc = 1)
    return Nodes.PyClassDefNode(pos,
        name = class_name,
        bases = ExprNodes.TupleNode(pos, args = base_list),
        doc = doc, body = body)

def p_c_class_definition(s, pos,  ctx):
    # s.sy == 'class'
    s.next()
    module_path = []
    class_name = p_ident(s)
    while s.sy == '.':
        s.next()
        module_path.append(class_name)
        class_name = p_ident(s)
    if module_path and ctx.visibility != 'extern':
        error(pos, "Qualified class name only allowed for 'extern' C class")
    if module_path and s.sy == 'IDENT' and s.systring == 'as':
        s.next()
        as_name = p_ident(s)
    else:
        as_name = class_name
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
        if ctx.visibility not in ('public', 'extern'):
            error(s.position(), "Name options only allowed for 'public' or 'extern' C class")
        objstruct_name, typeobj_name = p_c_class_options(s)
    if s.sy == ':':
        if ctx.level == 'module_pxd':
            body_level = 'c_class_pxd'
        else:
            body_level = 'c_class'
        doc, body = p_suite(s, Ctx(level = body_level), with_doc = 1)
    else:
        s.expect_newline("Syntax error in C class definition")
        doc = None
        body = None
    if ctx.visibility == 'extern':
        if not module_path:
            error(pos, "Module name required for 'extern' C class")
        if typeobj_name:
            error(pos, "Type object name specification not allowed for 'extern' C class")
    elif ctx.visibility == 'public':
        if not objstruct_name:
            error(pos, "Object struct name specification required for 'public' C class")
        if not typeobj_name:
            error(pos, "Type object name specification required for 'public' C class")
    elif ctx.visibility == 'private':
        if ctx.api:
            error(pos, "Only 'public' C class can be declared 'api'")
    else:
        error(pos, "Invalid class visibility '%s'" % ctx.visibility)
    return Nodes.CClassDefNode(pos,
        visibility = ctx.visibility,
        typedef_flag = ctx.typedef_flag,
        api = ctx.api,
        module_name = ".".join(module_path),
        class_name = class_name,
        as_name = as_name,
        base_class_module = base_class_module,
        base_class_name = base_class_name,
        objstruct_name = objstruct_name,
        typeobj_name = typeobj_name,
        in_pxd = ctx.level == 'module_pxd',
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
    doc, body = p_suite(s, Ctx(level = 'property'), with_doc = 1)
    return Nodes.PropertyNode(pos, name = name, doc = doc, body = body)

def p_doc_string(s):
    if s.sy == 'BEGIN_STRING':
        pos = s.position()
        kind, result = p_cat_string_literal(s)
        if s.sy != 'EOF':
            s.expect_newline("Syntax error in doc string")
        if kind != 'u':
            # warning(pos, "Python 3 requires docstrings to be unicode strings")
            if kind == 'b':
                result.encoding = None # force a unicode string
        return result
    else:
        return None
        
def p_code(s, level=None):
    body = p_statement_list(s, Ctx(level = level), first_statement = 1)
    if s.sy != 'EOF':
        s.error("Syntax error in statement [%s,%s]" % (
            repr(s.sy), repr(s.systring)))
    return body

COMPILER_DIRECTIVE_COMMENT_RE = re.compile(r"^#\s*cython:\s*(\w+)\s*=(.*)$")

def p_compiler_directive_comments(s):
    result = {}
    while s.sy == 'commentline':
        m = COMPILER_DIRECTIVE_COMMENT_RE.match(s.systring)
        if m:
            name = m.group(1)
            try:
                value = Options.parse_option_value(str(name), str(m.group(2).strip()))
                if value is not None: # can be False!
                    result[name] = value
            except ValueError, e:
                s.error(e.args[0], fatal=False)
        s.next()
    return result

def p_module(s, pxd, full_module_name):
    pos = s.position()

    option_comments = p_compiler_directive_comments(s)
    s.parse_comments = False

    doc = p_doc_string(s)
    if pxd:
        level = 'module_pxd'
    else:
        level = 'module'

    body = p_statement_list(s, Ctx(level = level), first_statement = 1)
    if s.sy != 'EOF':
        s.error("Syntax error in statement [%s,%s]" % (
            repr(s.sy), repr(s.systring)))
    return ModuleNode(pos, doc = doc, body = body,
                      full_module_name = full_module_name,
                      option_comments = option_comments)

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

