"""
A simple XPath-like language for tree traversal.

This works by creating a filter chain of generator functions.  Each
function selects a part of the expression, e.g. a child node, a
specific descendant or a node that holds an attribute.
"""

import re

path_tokenizer = re.compile(
    "("
    "'[^']*'|\"[^\"]*\"|"
    "//?|"
    "\(\)|"
    "==?|"
    "[/.*\[\]\(\)@])|"
    "([^/\[\]\(\)@=\s]+)|"
    "\s+"
    ).findall

def iterchildren(node, attr_name):
    # returns an iterable of all child nodes of that name
    child = getattr(node, attr_name)
    if child is not None:
        if type(child) is list:
            return child
        else:
            return [child]
    else:
        return ()

def _get_first_or_none(it):
    try:
        try:
            _next = it.next
        except AttributeError:
            return next(it)
        else:
            return _next()
    except StopIteration:
        return None

def type_name(node):
    return node.__class__.__name__.split('.')[-1]

def parse_func(next, token):
    name = token[1]
    token = next()
    if token[0] != '(':
        raise ValueError("Expected '(' after function name '%s'" % name)
    predicate = handle_predicate(next, token, end_marker=')')
    return name, predicate

def handle_func_not(next, token):
    """
    func(...)
    """
    name, predicate = parse_func(next, token)

    def select(result):
        for node in result:
            if _get_first_or_none(predicate(node)) is not None:
                yield node
    return select

def handle_name(next, token):
    """
    /NodeName/
    or
    func(...)
    """
    name = token[1]
    if name in functions:
        return functions[name](next, token)
    def select(result):
        for node in result:
            for attr_name in node.child_attrs:
                for child in iterchildren(node, attr_name):
                    if type_name(child) == name:
                        yield child
    return select

def handle_star(next, token):
    """
    /*/
    """
    def select(result):
        for node in result:
            for name in node.child_attrs:
                for child in iterchildren(node, name):
                    yield child
    return select

def handle_dot(next, token):
    """
    /./
    """
    def select(result):
        return result
    return select

def handle_descendants(next, token):
    """
    //...
    """
    token = next()
    if token[0] == "*":
        def iter_recursive(node):
            for name in node.child_attrs:
                for child in iterchildren(node, name):
                    yield child
                    for c in iter_recursive(child):
                        yield c
    elif not token[0]:
        node_name = token[1]
        def iter_recursive(node):
            for name in node.child_attrs:
                for child in iterchildren(node, name):
                    if type_name(child) == node_name:
                        yield child
                    for c in iter_recursive(child):
                        yield c
    else:
        raise ValueError("Expected node name after '//'")

    def select(result):
        for node in result:
            for child in iter_recursive(node):
                yield child
                    
    return select

def handle_attribute(next, token):
    token = next()
    if token[0]:
        raise ValueError("Expected attribute name")
    name = token[1]
    token = next()
    value = None
    if token[0] == '=':
        value = parse_path_value(next)
    if value is None:
        def select(result):
            for node in result:
                try:
                    attr_value = getattr(node, name)
                except AttributeError:
                    continue
                if attr_value is not None:
                    yield attr_value
    else:
        def select(result):
            for node in result:
                try:
                    attr_value = getattr(node, name)
                except AttributeError:
                    continue
                if attr_value == value:
                    yield value
    return select

def parse_path_value(next):
    token = next()
    value = token[0]
    if value[:1] == "'" or value[:1] == '"':
        value = value[1:-1]
    else:
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Invalid attribute predicate: '%s'" % value)
    return value

def handle_predicate(next, token, end_marker=']'):
    token = next()
    selector = []
    while token[0] != end_marker:
        selector.append( operations[token[0]](next, token) )
        try:
            token = next()
        except StopIteration:
            break
        else:
            if token[0] == "/":
                token = next()

    def select(result):
        for node in result:
            subresult = iter((node,))
            for select in selector:
                subresult = select(subresult)
            predicate_result = _get_first_or_none(subresult)
            if predicate_result is not None:
                yield predicate_result
    return select

operations = {
    "@":  handle_attribute,
    "":   handle_name,
    "*":  handle_star,
    ".":  handle_dot,
    "//": handle_descendants,
    "[":  handle_predicate,
    }

functions = {
    'not' : handle_func_not
    }

def _build_path_iterator(path):
    # parse pattern
    stream = iter([ (special,text)
                    for (special,text) in path_tokenizer(path)
                    if special or text ])
    try:
        _next = stream.next
    except AttributeError:
        # Python 3
        def _next():
            return next(stream)
    token = _next()
    selector = []
    while 1:
        try:
            selector.append(operations[token[0]](_next, token))
        except StopIteration:
            raise ValueError("invalid path")
        try:
            token = _next()
            if token[0] == "/":
                token = _next()
        except StopIteration:
            break
    return selector

# main module API

def iterfind(node, path):
    selector_chain = _build_path_iterator(path)
    result = iter((node,))
    for select in selector_chain:
        result = select(result)
    return result

def find_first(node, path):
    return _get_first_or_none(iterfind(node, path))

def find_all(node, path):
    return list(iterfind(node, path))
