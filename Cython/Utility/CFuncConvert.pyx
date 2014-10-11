#################### cfunc.to_py ####################

@cname("{{cname}}")
cdef object {{cname}}({{return_type.ctype}} (*f)({{ ', '.join(arg.type_cname for arg in args) }}) {{except_clause}}):
    def wrap({{ ', '.join('{arg.ctype} {arg.name}'.format(arg=arg) for arg in args) }}):
        """wrap({{', '.join(('{arg.name}: {arg.type_displayname}'.format(arg=arg) if arg.type_displayname else arg.name) for arg in args)}}){{if return_type.type_displayname}} -> {{return_type.type_displayname}}{{endif}}"""
        {{'' if return_type.type.is_void else 'return '}}f({{ ', '.join(arg.name for arg in args) }})
    return wrap
