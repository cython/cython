# Used to generate tests/run/test_dataclasses.pyx but translating the CPython test suite
# dataclass file. Initially run using Python 3.10 - this file is not designed to be
# backwards compatible since it will be run manually and infrequently.

import ast
import os.path
import sys

unavailable_functions = frozenset({
    'dataclass_textanno',  # part of CPython test module
    'dataclass_module_1',  # part of CPython test module
    'make_dataclass',  # not implemented in Cython dataclasses (probably won't be implemented)
})

skip_tests = frozenset({
    # needs Cython compile
    ('TestCase', 'test_field_default_default_factory_error'),
    ('TestCase', 'test_two_fields_one_default'),
    ('TestCase', 'test_overwrite_hash'),
    ('TestCase', 'test_eq_order'),
    ('TestCase', 'test_no_unhashable_default'),
    ('TestCase', 'test_disallowed_mutable_defaults'),
    ('TestCase', 'test_classvar_default_factory'),
    ('TestCase', 'test_field_metadata_mapping'),
    ('TestFieldNoAnnotation', 'test_field_without_annotation'),
    ('TestFieldNoAnnotation', 'test_field_without_annotation_but_annotation_in_base'),
    ('TestFieldNoAnnotation', 'test_field_without_annotation_but_annotation_in_base_not_dataclass'),
    ('TestOrdering', 'test_overwriting_order'),
    ('TestHash', 'test_hash_rules'),
    ('TestHash', 'test_hash_no_args'),
    ('TestFrozen', 'test_inherit_nonfrozen_from_empty_frozen'),
    ('TestFrozen', 'test_inherit_nonfrozen_from_frozen'),
    ('TestFrozen', 'test_inherit_frozen_from_nonfrozen'),
    ('TestFrozen', 'test_overwriting_frozen'),
    ('TestSlots', 'test_add_slots_when_slots_exists'),
    ('TestSlots', 'test_cant_inherit_from_iterator_slots'),
    ('TestSlots', 'test_weakref_slot_without_slot'),
    ('TestKeywordArgs', 'test_no_classvar_kwarg'),
    ('TestKeywordArgs', 'test_KW_ONLY_twice'),
    ('TestKeywordArgs', 'test_defaults'),
    # uses local variable in class definition
    ('TestCase', 'test_default_factory'),
    ('TestCase', 'test_default_factory_with_no_init'),
    ('TestCase', 'test_field_default'),
    ('TestCase', 'test_function_annotations'),
    ('TestDescriptors', 'test_lookup_on_instance'),
    ('TestCase', 'test_default_factory_not_called_if_value_given'),
    ('TestCase', 'test_class_attrs'),
    ('TestStringAnnotations',),  # almost all the texts here use local variables

    # Currently unsupported
    ('TestOrdering', 'test_functools_total_ordering'),  # combination of cython dataclass and total_ordering
    ('TestCase', 'test_missing_default_factory'),  # we're MISSING MISSING
    ('TestCase', 'test_missing_default'),  # MISSING
    ('TestCase', 'test_missing_repr'),  # MISSING
    ('TestSlots',),  # __slots__ isn't understood
    ('TestMatchArgs',),
    ('TestKeywordArgs', 'test_field_marked_as_kwonly'),
    ('TestKeywordArgs', 'test_match_args'),
    ('TestKeywordArgs', 'test_KW_ONLY'),
    ('TestKeywordArgs', 'test_KW_ONLY_as_string'),
    ('TestKeywordArgs', 'test_post_init'),
    ('TestCase', 'test_class_var_frozen'),  # __annotations__ not present on cdef classes https://github.com/cython/cython/issues/4519
    ('TestCase', 'test_dont_include_other_annotations'),  # __annotations__
    ('TestDocString',),  # don't think cython dataclasses currently set __doc__

    # either cython.dataclasses.field or cython.dataclasses.dataclass called directly as functions
    # (will probably never be supported)
    ('TestCase', 'test_field_repr'),
    ('TestCase', 'test_dynamic_class_creation'),
    ('TestCase', 'test_dynamic_class_creation_using_field'),

    # Requires inheritance from non-cdef class
    ('TestCase', 'test_is_dataclass_genericalias'),
    ('TestCase', 'test_generic_extending'),
    ('TestCase', 'test_generic_dataclasses'),
    ('TestCase', 'test_generic_dynamic'),
    ('TestInit', 'test_inherit_from_protocol'),
    ('TestAbstract', 'test_abc_implementation'),
    ('TestAbstract', 'test_maintain_abc'),
    # Requires multiple inheritance from extension types (or to identify the second base and make it a regular class)
    ('TestCase', 'test_post_init_not_auto_added'),
    ('TestCase', 'test_helper_asdict_namedtuple_derived'),
    # Refers to nonlocal from enclosing function
    ('TestCase', 'test_post_init_staticmethod'),  # TODO replicate the gist of the test elsewhere
    # difficult to translate the test, requires non-cdef class
    ('TestCase', 'test_deliberately_mutable_defaults'),
    ('TestCase', 'test_is_dataclass_when_getattr_always_returns'),
    ('TestDescriptors', 'test_non_descriptor'),
    ('TestDescriptors', 'test_set_name'),
    ('TestDescriptors', 'test_setting_field_calls_set'),
    ('TestDescriptors', 'test_setting_uninitialized_descriptor_field'),
    # Looks up __dict__, which cdef classes don't typically have
    ('TestCase', 'test_init_false_no_default'),
    ('TestCase', 'test_init_var_inheritance'),  # __dict__ again
    ('TestCase', 'test_base_has_init'),
    ('TestInit', 'test_base_has_init'),  # needs __dict__ for vars
    # Requires arbitrary attributes to be writeable
    ('TestCase', 'test_post_init_super'),
    # Cython being strict about argument types - expected difference
    ('TestDescriptors', 'test_getting_field_calls_get'),
    ('TestDescriptors', 'test_init_calls_set'),
    ('TestHash', 'test_eq_only'),
    # I think an expected difference with cdef classes - the property will be in the dict
    ('TestCase', 'test_items_in_dicts'),
    # These tests are probably fine, but the string substitution in this file doesn't get it right
    ('TestRepr', 'test_repr'),
    ('TestCase', 'test_not_in_repr'),
    ('TestRepr', 'test_no_repr'),
    # class variable doesn't exist in Cython so uninitialized variable appears differently - for now this is deliberate
    ('TestInit', 'test_no_init'),
    # I believe the test works but the ordering functions do appear in the class dict (and default slot wrappers which
    # just raise NotImplementedError
    ('TestOrdering', 'test_no_order'),

    # Bugs
    ('TestCase', 'test_no_options'),  # @dataclass()
    ('TestCase', 'test_field_no_default'),  # field()
    ('TestCase', 'test_init_in_order'),  # field()
    ('TestCase', 'test_hash_field_rules'),  # compiler crash
    ('TestCase', 'test_class_var'),  # not sure but compiler crash
    ('TestCase', 'test_field_order'),  # invalid C code (__pyx_base?)
    ('TestCase', 'test_overwrite_fields_in_derived_class'),  # invalid C code (__pyx_base?)
    ('TestReplace', 'test_recursive_repr'),  # recursion error
    ('TestReplace', 'test_recursive_repr_two_attrs'),  # recursion error
    ('TestReplace', 'test_recursive_repr_misc_attrs'),  # recursion error
    ('TestReplace', 'test_recursive_repr_indirection'),  # recursion error
    ('TestReplace', 'test_recursive_repr_indirection_two'),  # recursion error
    ('TestCase', 'test_intermediate_non_dataclass'),  # issue with propagating through intermediate class
    ('TestFrozen',),  # raises AttributeError, not FrozenInstanceError (may be hard to fix)
    ('TestReplace', 'test_frozen'),  # AttributeError not FrozenInstanceError
    ('TestCase', 'test_post_init'),  # Works except for AttributeError instead of FrozenInstanceError
    ('TestCase', 'test_dataclasses_qualnames'),  # doesn't define __setattr__ and just relies on Cython to enforce readonly properties
    ('TestCase', 'test_compare_subclasses'),  # wrong comparison
    ('TestCase', 'test_simple_compare'),  # wrong comparison
    ('TestCase', 'test_field_named_self'),  # I think just an error in inspecting the signature
    ('TestCase', 'test_init_var_default_factory'),  # should be raising a compile error
    ('TestCase', 'test_init_var_no_default'),  # should be raising a compile error
    ('TestCase', 'test_init_var_with_default'),  # not sure...
    ('TestReplace', 'test_initvar_with_default_value'),  # needs investigating
    

    # Maybe bugs?
    # non-default argument 'z' follows default argument in dataclass __init__ - this message looks right to me!
    ('TestCase', 'test_class_marker'),
    # cython.dataclasses.field parameter 'metadata' must be a literal value - possibly not something we can support?
    ('TestCase', 'test_field_metadata_custom_mapping'),
    ('TestCase', 'test_class_var_default_factory'),  # possibly to do with ClassVar being assigned a field
    ('TestCase', 'test_class_var_with_default'),  # possibly to do with ClassVar being assigned a field
    ('TestDescriptors',),  # mostly don't work - I think this may be a limitation of cdef classes but needs investigating
})

class DataclassInDecorators(ast.NodeVisitor):
    found = False
    def visit_Name(self, node):
        if node.id == "dataclass":
            self.found = True
        return self.generic_visit(node)

    def generic_visit(self, node):
        if self.found:
            return  # skip
        return super().generic_visit(node)

def dataclass_in_decorators(decorator_list):
    finder = DataclassInDecorators()
    for dec in decorator_list:
        finder.visit(dec)
        if finder.found:
            return True
    return False


class SubstituteNameString(ast.NodeTransformer):
    def __init__(self, substitutions):
        super().__init__()
        self.substitutions = substitutions

    def visit_Constant(self, node):
        # attempt to handle some difference in class names
        # (note: requires Python>=3.8)
        if isinstance(node.value, str):
            if node.value.find("<locals>") != -1:
                import re
                new_value = re.sub("[\w.]*<locals>", "", node.value)
                for key, value in self.substitutions.items():
                    new_value2 = re.sub(f"(?<![\w])[.]{key}(?![\w])", value, new_value)
                    if new_value != new_value2:
                        node.value = new_value2
                        break
        return node


class SubstituteName(SubstituteNameString):
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):  # don't reassign lhs
            return node
        replacement = self.substitutions.get(node.id, None)
        if replacement is not None:
            return ast.Name(id=replacement, ctx=node.ctx)
        else:
            return node


class ExtraDataclassesToTopLevel(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.nested_name = []
        self.current_function_global_classes = []
        self.global_classes = []
        self.used_names = set()
        self.collected_substitutions = {}
        self.uses_unavailable_name = False
        self.top_level_class = True

    def visit_ClassDef(self, node):
        if not self.top_level_class or dataclass_in_decorators(node.decorator_list):
            # Include any non-toplevel class in this to be able
            # to test inheritance.

            self.generic_visit(node)  # any nested classes in it?
            if not node.body:
                node.body.append(ast.Pass)

            # First, make it a C class. 
            node.decorator_list.append(ast.Name(id="cclass", ctx=ast.Load()))
            # change the name
            old_name = node.name
            new_name = "_".join([node.name] + self.nested_name)
            while new_name in self.used_names:
                new_name = new_name + "_"
            node.name = new_name
            self.current_function_global_classes.append(node)
            self.used_names.add(new_name)
            # hmmmm... possibly there's a few cases where there's more than one name?
            self.collected_substitutions[old_name] = node.name
            return ast.Assign(
                targets=[ ast.Name(id=old_name, ctx=ast.Store()) ],
                value=ast.Name(id=new_name, ctx=ast.Load()),
                lineno=-1
            )
        else:
            top_level_class, self.top_level_class = self.top_level_class, False
            self.nested_name.append(node.name)
            if tuple(self.nested_name) in skip_tests:
                self.top_level_class = top_level_class
                self.nested_name.pop()
                return None
            self.generic_visit(node)
            self.nested_name.pop()
            if not node.body:
                node.body.append(ast.Pass())
            self.top_level_class = top_level_class
            return node

    def visit_FunctionDef(self, node):
        self.nested_name.append(node.name)
        if tuple(self.nested_name) in skip_tests:
            self.nested_name.pop()
            return None
        collected_subs, self.collected_substitutions = self.collected_substitutions, {}
        uses_unavailable_name, self.uses_unavailable_name = self.uses_unavailable_name, False
        current_func_globs, self.current_function_global_classes = self.current_function_global_classes, []

        # visit once to work out what the substitutions should be
        self.generic_visit(node)
        if self.collected_substitutions:
            # replace strings in this function
            node = SubstituteNameString(self.collected_substitutions).visit(node)
            replacer = SubstituteName(self.collected_substitutions)
            # replace any base classes
            for global_class in self.current_function_global_classes:
                global_class = replacer.visit(global_class)
        self.global_classes.append(self.current_function_global_classes)

        self.nested_name.pop()
        self.collected_substitutions = collected_subs
        if self.uses_unavailable_name:
            node = None
        self.uses_unavailable_name = uses_unavailable_name
        self.current_function_global_classes = current_func_globs
        return node

    def visit_Name(self, node):
        if node.id in unavailable_functions:
            self.uses_unavailable_name = True
        return self.generic_visit(node)

    def visit_Import(self, node):
        return None  # drop imports, we add these into the text ourself

    def visit_ImportFrom(self, node):
        return None  # drop imports, we add these into the text ourself

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "assertRaisesRegex":
            # we end up with a bunch of subtle name changes that are very hard to correct for
            # therefore, replace with "assertRaises"
            node.func.attr = "assertRaises"
            node.args.pop()
        return self.generic_visit(node)

    def visit_Module(self, node):
        self.generic_visit(node)
        node.body[0:0] = self.global_classes
        return node

def main():
    script_path = os.path.split(sys.argv[0])[0]
    filename = "test_dataclasses.py"
    py_module_path = os.path.join(script_path, "dataclass_test_data", filename)
    with open(py_module_path, "r") as f:
        tree = ast.parse(f.read(), filename)

    transformer = ExtraDataclassesToTopLevel()
    tree = transformer.visit(tree)

    output_path = os.path.join(script_path, "..", "tests", "run", filename+"x")
    with open(output_path, "w") as f:
        print("# AUTO-GENERATED BY Tools/make_dataclass_tests.py", file=f)
        print("# DO NOT EDIT", file=f)
        print(file=f)
        print("# cython: language_level=3", file=f)  # doesn't look like it goes in the include
        # any extras Cython needs to add go in this include file
        print('include "test_dataclasses.pxi"', file=f)
        print(file=f)
        print(ast.unparse(tree), file=f)
    

if __name__ == "__main__":
    main()